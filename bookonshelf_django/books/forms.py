from django import forms
from .models import Genres, Languages, Writers
from django.forms import ModelForm



class WritersForm(ModelForm):
    class Meta:
        model = Writers
        fields = ['writername']
        widgets = {
            'writername': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Автор'
            }),
        }


