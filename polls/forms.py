from django import forms

class InputForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    roll_number = forms.IntegerField(help_text="Enter 6 digit roll number")
    password = forms.CharField(widget=forms.PasswordInput)
    
from .models import FormModel

class FormModelForm(forms.ModelForm):
    class Meta:
        model= FormModel
        fields = "__all__"