from django import forms
from .models import ProjectBillingRate

from .models import Invoice


class ProjectBillingRateForm(forms.ModelForm):

    class Meta:
        model = ProjectBillingRate
        fields = [
            'project_site',
            'billing_designation',
            'hourly_rate'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'




class GenerateInvoiceForm(forms.Form):

    invoice_no = forms.CharField(
        max_length=50,
        label='Invoice Number'
    )

    invoice_date = forms.DateField(
        label='Invoice Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    lpo_no = forms.CharField(
        max_length=50,
        required=False,
        label='LPO Number'
    )

    payment_terms = forms.CharField(
        max_length=100,
        required=False,
        label='Payment Terms'
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    terms_conditions = forms.CharField(
        required=False,
        label='Terms & Conditions',
        widget=forms.Textarea(attrs={'rows': 4})
    )

    checked_by = forms.CharField(
        max_length=100,
        required=False
    )

    checked_by_designation = forms.CharField(
        max_length=100,
        required=False
    )

    approved_by = forms.CharField(
        max_length=100,
        required=False
    )

    approved_by_designation = forms.CharField(
        max_length=100,
        required=False
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class InvoiceEditForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = [
            'invoice_no',
            'invoice_date',
            'lpo_no',
            'payment_terms',
            'description',
            'terms_conditions',
            'checked_by',
            'checked_by_designation',
            'approved_by',
            'approved_by_designation',
            'remarks',
        ]

        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'terms_conditions': forms.Textarea(attrs={'rows': 4}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'