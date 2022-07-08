import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

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
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    foreign = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Car
        fields = ("registration", "foreign", "brand", "model")

    def clean_registration(self):
        data = self.cleaned_data['registration']
        # noinspection RegExpSimplifiable
        matched = re.match("[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}", data)
        if not matched:
            raise ValidationError("Registration must have 'xx-xx-xx' format beeing 'x' an number or a capital letter.")
        return data
