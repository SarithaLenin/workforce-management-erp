from django import forms
from .models import *

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'email' : forms.EmailInput(
                attrs={'placeholder':'example@company.com'}
            ),
            'trade_license_expiry':forms.DateInput(
                attrs={'type' : 'date'}
            ),
            'address' :forms.Textarea(
                attrs={ 'rows' : 3}
            ),

            # 'is_active' : forms.CheckboxInput(
            #     attrs={'class' : 'form-check-input'}
            # ),
            
        }

    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs['class']='form-check-input'
            elif name == 'logo':
                 field.widget.attrs['class']='form-control'
            else:
               field.widget.attrs['class']='form-control'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            digits = ''.join(filter(str.isdigit,phone))

            if len(digits) < 9 or len(digits) > 15:
                raise forms.ValidationError("phone number must contain 9 to 15 digits.")
        
        return phone



