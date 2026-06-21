from django.db import models
from companies.models import Company
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Designation(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    SALARY_TYPE_CHOICES = (
        ('BASIC', 'Basic Salary'),
        ('HOURLY', 'Hourly Based'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    # --------------------
    # BASIC INFO
    # --------------------
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    employee_id = models.CharField(max_length=10, unique=True)

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)

    photo = models.ImageField(upload_to='employees/photos/', blank=True, null=True)

    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    nationality = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    joining_date = models.DateField(blank=True, null=True)

    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True
    )

    # --------------------
    # DOCUMENT NUMBERS (FAST VIEW)
    # --------------------
    passport_number = models.CharField(max_length=50, blank=True)
    emirates_id_number = models.CharField(max_length=50, blank=True)

    # --------------------
    # SALARY INFO
    # --------------------
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES)

    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # --------------------
    # STATUS
    # --------------------
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name}"
    


class EmployeeDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = (
        ('PASSPORT', 'Passport'),
        ('VISA', 'Visa'),
        ('EMIRATES_ID', 'Emirates ID'),
        ('LABOUR_CARD', 'Labour Card'),
        ('CONTRACT', 'Contract / Offer Letter'),
        ('OTHER', 'Other'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES
    )

    document_number = models.CharField(
        max_length=100,
        blank=True
    )

    issue_date = models.DateField(
        blank=True,
        null=True
    )

    expiry_date = models.DateField(
        blank=True,
        null=True
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

   
    def expiry_status(self):
        if not self.expiry_date:
            return "No Expiry"

        today = timezone.now().date()
        expiring_limit = today + timedelta(days=30)

        if self.expiry_date < today:
            return "Expired"
        elif self.expiry_date <= expiring_limit:
            return "Expiring Soon"
        else:
            return "Valid"


    def expiry_badge_class(self):
        status = self.expiry_status()

        if status == "Expired":
            return "bg-danger"
        elif status == "Expiring Soon":
            return "bg-warning text-dark"
        elif status == "Valid":
            return "bg-success"
        else:
            return "bg-secondary"

    def __str__(self):
        return f"{self.employee.first_name} - {self.get_document_type_display()}"

class EmployeeDocumentFile(models.Model):

    document = models.ForeignKey(
        EmployeeDocument,
        on_delete=models.CASCADE,
        related_name='files'
    )

    file_title = models.CharField(
        max_length=100,
        blank=True
    )

    file = models.FileField(
        upload_to='employee_documents/'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_title or self.file.name    

  
