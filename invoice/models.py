from django.db import models
from clients.models import ProjectSite
from employees.models import Designation
from django.core.validators import MinValueValidator
from companies.models import Company
from timesheet.models import MonthlyTimesheet



# Create your models here.




class ProjectBillingRate(models.Model):

    project_site = models.ForeignKey(
        ProjectSite,
        on_delete=models.CASCADE
    )

    billing_designation = models.ForeignKey(
        Designation,
        on_delete=models.CASCADE
    )

    hourly_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    class Meta:
        unique_together = (
            'project_site',
            'billing_designation'
        )

    def __str__(self):
        return f"{self.project_site.name} - {self.billing_designation.name}"
    


class Invoice(models.Model):

    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
    )

    invoice_no = models.CharField(
        max_length=50,
        unique=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT
    )

    timesheet = models.OneToOneField(
        MonthlyTimesheet,
        on_delete=models.PROTECT,blank=True,null=True
    )

    invoice_date = models.DateField()
    lpo_no = models.CharField(max_length=50, blank=True, null=True)

    payment_terms = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    terms_conditions = models.TextField(blank=True, null=True)

    checked_by = models.CharField(max_length=100, blank=True, null=True)

    checked_by_designation = models.CharField(max_length=100, blank=True, null=True)

    approved_by = models.CharField(max_length=100, blank=True, null=True)

    approved_by_designation = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    paid_date = models.DateField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_no



class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT
    )

    qty = models.IntegerField()

    total_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    taxable_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    vat_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    net_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.invoice.invoice_no} - {self.designation.name}"