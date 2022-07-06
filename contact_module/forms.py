from django import forms
from .models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'phone', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control dl',
                'id': 'name',
                'placeholder': 'نام شما',

            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control dl',
                'id': 'email',
                'placeholder': 'شماره تلفن',
            },
            ),
            'subject': forms.TextInput(attrs={
                'class': 'form-control dl',
                'id': 'subject',
                'placeholder': 'موضوع',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control dl',
                'id': 'message',
                'rows': '5',
                'style': 'height: 150px',
                'placeholder': 'پیام شما',
            })
        }

        labels = {
            'full_name': 'نام و نام خانوادگی شما',
            'phone': 'شماره شما'
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
            }
        }
        validators = {
            'phone': {
                'required': 'شماره تلفن اجباری می باشد. لطفا وارد کنید',
                'regex': '^(\+98|0)?9\d{9}$'
            }
        }
