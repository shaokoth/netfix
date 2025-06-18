from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    birth =forms.DateField(
        widget=DateInput(),
        help_text="Enter your date of birth",
    )

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2', 'birth')
        widgets = {
             'username': forms.TextInput(attrs={
                'placeholder': 'Enter Username',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter Password',
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        })
          
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user, birth=self.cleaned_data.get('birth'))
        return user


class CompanySignUpForm(UserCreationForm):
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,
        help_text='Choose your company field'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter Username',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email',
                'class': 'form-control'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add attributes to password1 and password2 manually
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter Password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })

        # Optional: style the custom 'field' dropdown
        self.fields['field'].widget.attrs.update({
            'class': 'form-select'  # Bootstrap 5 compatible
        })
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user, field=self.cleaned_data.get('field'))
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        })
    )