from django import forms
from .models import QuestionAndAnswer


class QuestionAndAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAndAnswer
        fields = ['question','name']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'question': 'سوال',
            'name': 'نام',
        }
        help_texts = {
            'question': '',
            'name': '',
        }
        error_messages = {
            'question': {
                'required': 'سوال را وارد کنید',
            },

            'name': {
                'required': 'نام را وارد کنید',
            },
        }

