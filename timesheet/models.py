from django.db import models
from companies.models import Company
from clients.models import ProjectSite
from employees.models import Employee

# Create your models here.


class MonthlyTimesheet(models.Model):

    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('APPROVED', 'Approved'),
    )

    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    project_site = models.ForeignKey(ProjectSite, on_delete=models.PROTECT)

    MONTH_CHOICES = (
        (1, 'JAN'),
        (2, 'FEB'),
        (3, 'MAR'),
        (4, 'APR'),
        (5, 'MAY'),
        (6, 'JUN'),
        (7, 'JUL'),
        (8, 'AUG'),
        (9, 'SEP'),
        (10, 'OCT'),
        (11, 'NOV'),
        (12, 'DEC'),
    )

    month = models.PositiveIntegerField(
        choices=MONTH_CHOICES
)
    year = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project_site', 'month', 'year')

    def __str__(self):
        return f"{self.project_site.name} - {self.month}/{self.year}"




class MonthlyTimesheetRow(models.Model):

    timesheet = models.ForeignKey(
        MonthlyTimesheet,
        on_delete=models.CASCADE,
        related_name='rows'
    )

    employee_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=100, blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT, null=True, blank=True)

    day_1 = models.CharField(max_length=10, blank=True)
    day_2 = models.CharField(max_length=10, blank=True)
    day_3 = models.CharField(max_length=10, blank=True)
    day_4 = models.CharField(max_length=10, blank=True)
    day_5 = models.CharField(max_length=10, blank=True)
    day_6 = models.CharField(max_length=10, blank=True)
    day_7 = models.CharField(max_length=10, blank=True)
    day_8 = models.CharField(max_length=10, blank=True)
    day_9 = models.CharField(max_length=10, blank=True)
    day_10 = models.CharField(max_length=10, blank=True)
    day_11 = models.CharField(max_length=10, blank=True)
    day_12 = models.CharField(max_length=10, blank=True)
    day_13 = models.CharField(max_length=10, blank=True)
    day_14 = models.CharField(max_length=10, blank=True)
    day_15 = models.CharField(max_length=10, blank=True)
    day_16 = models.CharField(max_length=10, blank=True)
    day_17 = models.CharField(max_length=10, blank=True)
    day_18 = models.CharField(max_length=10, blank=True)
    day_19 = models.CharField(max_length=10, blank=True)
    day_20 = models.CharField(max_length=10, blank=True)
    day_21 = models.CharField(max_length=10, blank=True)
    day_22 = models.CharField(max_length=10, blank=True)
    day_23 = models.CharField(max_length=10, blank=True)
    day_24 = models.CharField(max_length=10, blank=True)
    day_25 = models.CharField(max_length=10, blank=True)
    day_26 = models.CharField(max_length=10, blank=True)
    day_27 = models.CharField(max_length=10, blank=True)
    day_28 = models.CharField(max_length=10, blank=True)
    day_29 = models.CharField(max_length=10, blank=True)
    day_30 = models.CharField(max_length=10, blank=True)
    day_31 = models.CharField(max_length=10, blank=True)

    total_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.employee_name
