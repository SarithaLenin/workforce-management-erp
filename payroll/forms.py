from django import forms
from django.utils import timezone

from companies.models import Company
from .models import ( Payroll, PayrollDeduction, PayrollPaymentBatch,)



class PayrollDeductionForm(forms.ModelForm):
    class Meta:
        model = PayrollDeduction
        fields = (
            "deduction_type",
            "amount",
            "remarks",
        )

        widgets = {
            "deduction_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),
            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional explanation",
                }
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Deduction amount must be greater than zero."
            )

        return amount
    



class PayrollEditForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = (
            "food_allowance",
            "absence_deduction_override",
            "manual_adjustment_reason",
        )

        labels = {
            "food_allowance": "Food Allowance",
            "absence_deduction_override": (
                "Final Absence Deduction"
            ),
            "manual_adjustment_reason": (
                "Reason for Manual Change"
            ),
        }

        widgets = {
            "food_allowance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "absence_deduction_override": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": (
                        "Leave empty for automatic calculation"
                    ),
                }
            ),
            "manual_adjustment_reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "Example: Approved sick leave"
                    ),
                }
            ),
        }

        help_texts = {
            "absence_deduction_override": (
                "Automatic deduction: absent days × AED 50. "
                "Enter 0 to waive it, or leave empty to use "
                "the automatic amount."
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        food_allowance = cleaned_data.get("food_allowance")
        absence_override = cleaned_data.get(
            "absence_deduction_override"
        )
        reason = cleaned_data.get(
            "manual_adjustment_reason",
            "",
        ).strip()

        food_changed = (
            food_allowance != self.instance.food_allowance
        )
        absence_changed = (
            absence_override
            != self.instance.absence_deduction_override
        )

        if (food_changed or absence_changed) and not reason:
            self.add_error(
                "manual_adjustment_reason",
                "Enter a reason for the manual change.",
            )

        return cleaned_data
    


class PayrollReopenForm(forms.Form):
    reason = forms.CharField(
        label="Reason for Reopening",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": (
                    "Explain why this payroll must be reopened"
                ),
            }
        ),
    )    




class PayrollPaymentFilterForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        empty_label="Select company",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )
    month = forms.ChoiceField(
        choices=(("", "Select month"),)
        + Payroll.MONTH_CHOICES,
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )
    year = forms.IntegerField(
        min_value=2020,
        max_value=2100,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["company"].queryset = (
            Company.objects.filter(
                is_active=True
            ).order_by("name")
        )

        if not self.is_bound:
            self.fields["year"].initial = (
                timezone.now().year
            )


class PayrollPaymentBatchForm(forms.ModelForm):
    class Meta:
        model = PayrollPaymentBatch
        fields = (
            "payment_method",
            "payment_date",
            "reference",
            "remarks",
        )

        widgets = {
            "payment_method": forms.Select(
                attrs={"class": "form-select"}
            ),
            "payment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "reference": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "WPS, bank or cheque reference"
                    ),
                }
            ),
            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional remarks",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.is_bound:
            self.fields["payment_date"].initial = (
                timezone.localdate()
            )

    def clean(self):
        cleaned_data = super().clean()

        method = cleaned_data.get("payment_method")
        reference = cleaned_data.get(
            "reference",
            "",
        ).strip()

        if method in ("WPS", "BANK", "CHEQUE") and not reference:
            self.add_error(
                "reference",
                "Enter the payment reference number.",
            )

        return cleaned_data
