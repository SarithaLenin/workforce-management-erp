from django.db import models
from employees.models import *


# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=50, unique=True)
    contact_person = models.CharField(max_length=25, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True, null=True)
    trn_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectSite(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    project_code = models.CharField(max_length=20,blank=True, null=True)
    name = models.CharField(max_length=50)
    lpo_number = models.CharField(max_length=50,blank=True, null=True)
    lpo_file =models.FileField(upload_to='project_sites/lpo/',blank=True, null=True) 
    quotation_file = models.FileField(upload_to='project_sites/quotations/',blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.name}"
   


class EmployeeAssignment(models.Model):

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    project_site = models.ForeignKey(
        ProjectSite,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    designation = models.ForeignKey(Designation , on_delete=models.PROTECT, blank=True,null=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.end_date:
            self.status = 'COMPLETED'
        else:
            self.status = 'ACTIVE'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} - {self.project_site.name}"