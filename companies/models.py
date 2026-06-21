from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=20,unique=True)
    trade_license_no = models.CharField(max_length=50)
    trade_license_expiry = models.DateField()
    trn_number = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    po_box = models.CharField(max_length=10,blank=True)
    logo = models.ImageField('company_logos/',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
        




