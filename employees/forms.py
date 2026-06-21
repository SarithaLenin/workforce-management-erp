from django import forms
from .models import *


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


from .models import EmployeeDocument


class EmployeeDocumentForm(forms.ModelForm):

    class Meta:
        model = EmployeeDocument
        fields = [
            'document_type',
            'document_number',
            'issue_date',
            'expiry_date',
            'remarks',
        ]

        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'