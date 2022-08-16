from email.policy import default
from django import forms


class FilesForm(forms.Form):
    srs_file = forms.FileField(required=False,allow_empty_file=True)
    platform_file = forms.FileField(required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class FilesForm_for_pipline(forms.Form):
    srs_file = forms.FileField(required=False,allow_empty_file=True)