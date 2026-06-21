from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from companies.models import Company
from employees.models import Employee


class Payroll(models.Model):
    MONTH_CHOICES = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    )

    SALARY_TYPES = (
        ("BASIC", "Basic Salary"),
        ("HOURLY", "Hourly Salary"),
    )

    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("APPROVED", "Approved"),
        ("PAID", "Paid"),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="payrolls",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="payrolls",
        null=True,
        blank=True,
    )

    month = models.PositiveSmallIntegerField(
        choices=MONTH_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    year = models.PositiveSmallIntegerField()

    salary_type = models.CharField(
        max_length=10,
        choices=SALARY_TYPES,
        default="HOURLY",
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    food_allowance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Basic-salary attendance
    absent_days = models.PositiveSmallIntegerField(default=0)
    absent_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("50.00"),
    )
    absence_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    calculated_absence_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    absence_deduction_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # Basic-salary overtime
    salary_days = models.PositiveSmallIntegerField(default=30)
    overtime_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    overtime_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    overtime_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    other_deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="generated_payrolls",
        null=True,
        blank=True,
    )


    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="approved_payrolls",
        null=True,
        blank=True,
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="paid_payrolls",
        null=True,
        blank=True,
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )


    reopened_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reopened_payrolls",
        null=True,
        blank=True,
    )

    reopened_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    reopen_reason = models.TextField(
        blank=True,
    )

    manual_adjustment_reason = models.TextField(
        blank=True,
    )

    manually_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="manually_updated_payrolls",
        null=True,
        blank=True,
    )

    manually_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-year", "-month", "employee__employee_id")
        constraints = [
            models.UniqueConstraint(
                fields=("employee", "month", "year"),
                name="unique_employee_monthly_payroll",
            )
        ]

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.get_month_display()} {self.year}"
        )


class PayrollDeduction(models.Model):
    DEDUCTION_TYPES = (
        ("ADVANCE", "Salary Advance"),
        ("VISA", "Visa Deduction"),
        ("OTHER", "Other Deduction"),
    )

    payroll = models.ForeignKey(
        Payroll,
        on_delete=models.CASCADE,
        related_name="deductions",
    )
    deduction_type = models.CharField(
        max_length=20,
        choices=DEDUCTION_TYPES,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return (
            f"{self.get_deduction_type_display()} - "
            f"AED {self.amount}"
        )
    


class PayrollPaymentBatch(models.Model):
    PAYMENT_METHODS = (
        ("WPS", "WPS"),
        ("BANK", "Bank Transfer"),
        ("CASH", "Cash"),
        ("CHEQUE", "Cheque"),
    )

    STATUS_CHOICES = (
        ("COMPLETED", "Completed"),
        ("REVERSED", "Reversed"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="payroll_payment_batches",
    )
    month = models.PositiveSmallIntegerField(
        choices=Payroll.MONTH_CHOICES,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )
    year = models.PositiveSmallIntegerField()

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
    )
    payment_date = models.DateField()
    reference = models.CharField(
        max_length=100,
        blank=True,
    )
    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    employee_count = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="COMPLETED",
    )

    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="processed_payroll_batches",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    reversed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reversed_payroll_batches",
        null=True,
        blank=True,
    )
    reversed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    reversal_reason = models.TextField(blank=True)

    class Meta:
        ordering = ("-payment_date", "-id")

    def __str__(self):
        return (
            f"PAY-{self.pk or 'NEW'} - "
            f"{self.company.name} - "
            f"{self.get_month_display()} {self.year}"
        )


class PayrollPaymentItem(models.Model):
    batch = models.ForeignKey(
        PayrollPaymentBatch,
        on_delete=models.PROTECT,
        related_name="items",
    )
    payroll = models.ForeignKey(
        Payroll,
        on_delete=models.PROTECT,
        related_name="payment_items",
    )
    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("batch", "payroll"),
                name="unique_payroll_in_payment_batch",
            )
        ]

    def __str__(self):
        return (
            f"{self.payroll.employee.employee_id} - "
            f"AED {self.paid_amount}"
        )    
    

