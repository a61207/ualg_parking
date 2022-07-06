from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, Client, RoleRequest, Car


class UserForm(UserCreationForm):
    CLIENT = 'CL'
    EMPLOYEE = 'EM'
    ADMINISTRATOR = 'AD'
    ROLES = [
        (CLIENT, 'Client'),
        (EMPLOYEE, 'Employee'),
        (ADMINISTRATOR, 'Administrator'),
    ]
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user = User.objects.create(username=user.email, email=user.email, password=user.password,
                                   last_name=user.last_name, first_name=user.first_name)
        Client.objects.create(user=user)
        if not self.cleaned_data['role'] == 'CL':
            RoleRequest.objects.create(user=user, role=self.cleaned_data['role'])
        if commit:
            user.save()
        return user


class RoleRequestForm(forms.ModelForm):
    ADMINISTRATOR = 'AD'
    EMPLOYEE = 'EM'
    ROLES = [
        (ADMINISTRATOR, 'Administrator'),
        (EMPLOYEE, 'Employee'),
    ]
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select())

    class Meta:
        model = RoleRequest
        fields = ("role",)


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ("registration", "foreign", "brand", "model")
