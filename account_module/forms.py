from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    phone = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'input100',
            'type': "text",
            'placeholder': "۰۹۲۱۰۰۰۱۲۳۴"

        }),
        validators=[
            validators.MaxLengthValidator(16),
            validators.RegexValidator(regex='^(\+98|0)?9\d{9}$', message='فرمت شماره تلفن صحیح نیست')
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'type': "password",
            'placeholder': "***********"
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'type': "password",
            'placeholder': "***********"
        }),
        validators=[
            validators.MaxLengthValidator(100),

        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class LoginForm(forms.Form):
    phone = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'input100',
            'type': "text",
            'placeholder': "۰۹۲۱۰۰۰۱۲۳۴"

        }),
        validators=[
            validators.MaxLengthValidator(16),
            validators.RegexValidator(regex='^(\+98|0)?9\d{9}$', message='فرمت شماره تلفن صحیح نیست')
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'type': "password",
            'placeholder': "***********"
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )


class ConfirmOtpForm(forms.Form):
    otp = forms.CharField(
        label='کد امنیتی',
        widget=forms.TextInput(attrs={
            'class': 'input100',
            'type': "text"
        }),
        validators=[
            validators.MaxLengthValidator(6)
        ]
    )


class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
             'class': 'input100',
            'type': "text",
            'placeholder': "۰۹۲۱۰۰۰۱۲۳۴"

        }),
        validators=[
            validators.MaxLengthValidator(16),
            validators.RegexValidator(regex='^(\+98|0)?9\d{9}$', message='فرمت شماره تلفن صحیح نیست')
        ]
    )


class ResendOtpForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'input100',
            'type': "text",
            'placeholder': "۰۹۲۱۰۰۰۱۲۳۴"

        }),
        validators=[
            validators.MaxLengthValidator(16),
            validators.RegexValidator(regex='^(\+98|0)?9\d{9}$', message='فرمت شماره تلفن صحیح نیست')
        ]
    )


class ResetPasswordForm(forms.Form):
    otp = forms.CharField(
        label='کد امنیتی',
        widget=forms.TextInput(attrs={
            'class': 'input100',
            'type': "text"
        }),
        validators=[
            validators.MaxLengthValidator(6)
        ]
    )

    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'type': "password"
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'type': "password"
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
