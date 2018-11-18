from django import forms


class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=200)
    role = forms.CharField(max_length=100)


class RegistrationTokenForm(forms.Form):
    token = forms.CharField(max_length=200)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    clinic_name = forms.CharField(max_length=300)
