from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Employee)
admin.site.register(Designation)
admin.site.register(EmployeeDocument)
admin.site.register(EmployeeDocumentFile)
