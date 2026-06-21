from django.db import models
from employees.models import Employee
from clients.models import ProjectSite, EmployeeAssignment

# Create your models here.

class DailyAttendance(models.Model):

    STATUS_CHOICES = (
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LEAVE', 'Leave'),
        ('HOLIDAY', 'Holiday'),
    )

    attendance_date = models.DateField()

    project_site = models.ForeignKey(
        ProjectSite,
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    assignment = models.ForeignKey(
        EmployeeAssignment,
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    total_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    remarks = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'attendance_date',
            'project_site',
            'employee',
        )

    def __str__(self):
        return f"{self.employee.first_name} - {self.attendance_date}"
