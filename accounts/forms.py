from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for field in self.fields.values():
        #     field.widget.attrs['class'] = 'form-control'

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input'
        })


class UserEditForm(forms.ModelForm):

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)

        super().__init__(*args, **kwargs)

        if user_profile:
            self.fields['role'].initial = user_profile.role

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'    



class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'         



class AdminResetPasswordForm(forms.Form):

    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label='New Password'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    


