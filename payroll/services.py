import calendar
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db.models import Sum

from timesheet.models import MonthlyTimesheetRow


ZERO = Decimal("0.00")
MONEY = Decimal("0.01")
NORMAL_HOURS = Decimal("8.00")


def round_money(value):
    return Decimal(value).quantize(
        MONEY,
        rounding=ROUND_HALF_UP,
    )


def read_hours(value):
    try:
        hours = Decimal(str(value).strip())
        return max(hours, ZERO)
    except (InvalidOperation, TypeError, ValueError):
        return ZERO


def get_attendance_summary(rows, total_days):
    daily_hours = {
        day: ZERO
        for day in range(1, total_days + 1)
    }
    absent_marked_days = set()

    for row in rows:
        for day in range(1, total_days + 1):
            value = getattr(row, f"day_{day}", "")
            code = str(value).strip().upper()

            if code == "A":
                absent_marked_days.add(day)
            else:
                daily_hours[day] += read_hours(value)

    # If hours exist on another project for the same day,
    # do not count that day as absent.
    absent_days = sum(
        1
        for day in absent_marked_days
        if daily_hours[day] == ZERO
    )

    total_hours = sum(
        daily_hours.values(),
        ZERO,
    )

    overtime_hours = sum(
        (
            max(hours - NORMAL_HOURS, ZERO)
            for hours in daily_hours.values()
        ),
        ZERO,
    )

    return {
        "total_hours": total_hours,
        "absent_days": absent_days,
        "overtime_hours": overtime_hours,
    }


def recalculate_payroll(payroll):
    if payroll.status != "DRAFT":
        raise ValidationError(
            "Only draft payroll can be recalculated."
        )

    rows = list(
        MonthlyTimesheetRow.objects.filter(
            employee=payroll.employee,
            timesheet__month=payroll.month,
            timesheet__year=payroll.year,
            timesheet__status="APPROVED",
        )
    )

    total_days = calendar.monthrange(
        payroll.year,
        payroll.month,
    )[1]

    summary = get_attendance_summary(
        rows,
        total_days,
    )

    payroll.salary_days = total_days

    other_deductions = (
        payroll.deductions.aggregate(
            total=Sum("amount")
        )["total"]
        or ZERO
    )

    if payroll.salary_type == "BASIC":
        salary_days = Decimal(total_days)

        overtime_rate = round_money(
            payroll.basic_salary
            / salary_days
            / NORMAL_HOURS
        )

        overtime_amount = round_money(
            summary["overtime_hours"]
            * overtime_rate
        )

        calculated_absence_deduction = round_money(
            Decimal(summary["absent_days"])
            * payroll.absent_rate
        )

        gross_salary = (
            payroll.basic_salary
            + payroll.food_allowance
            + overtime_amount
        )

        payroll.absent_days = summary["absent_days"]

        payroll.calculated_absence_deduction = (
            calculated_absence_deduction
        )

        if payroll.absence_deduction_override is None:
            payroll.absence_deduction = (
                calculated_absence_deduction
            )
        else:
            payroll.absence_deduction = round_money(
                payroll.absence_deduction_override
            )

        payroll.overtime_hours = (
            summary["overtime_hours"]
        )
        payroll.overtime_rate = overtime_rate
        payroll.overtime_amount = overtime_amount

    else:
        gross_salary = (
            summary["total_hours"]
            * payroll.hourly_rate
        )

        payroll.absent_days = 0
        payroll.calculated_absence_deduction = ZERO
        payroll.absence_deduction_override = None
        payroll.absence_deduction = ZERO

        payroll.overtime_hours = ZERO
        payroll.overtime_rate = ZERO
        payroll.overtime_amount = ZERO

    payroll.total_hours = summary["total_hours"]
    payroll.gross_salary = round_money(gross_salary)
    payroll.other_deductions = round_money(
        other_deductions
    )

    payroll.total_deductions = round_money(
        payroll.absence_deduction
        + payroll.other_deductions
    )

    payroll.net_salary = max(
        payroll.gross_salary
        - payroll.total_deductions,
        ZERO,
    )

    payroll.save()

    return payroll