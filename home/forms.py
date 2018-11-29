from django import forms


class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=200)
    role = forms.ChoiceField(choices=[('Dispatcher', 'Dispatcher'), ('Warehouse Personnel', 'Warehouse Personnel'), ('Clinic Manager', 'Clinic Manager')])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)


class RegistrationTokenForm(forms.Form):
    token = forms.CharField(max_length=200)


class RegistrationTokenAfterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class RegistrationTokenAfterForm_clinicManager(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    clinic_name = forms.CharField(max_length=300)


class ChangeInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=200)
