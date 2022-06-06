from django.contrib.auth.forms import UserCreationForm

from .models import User, Client


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user = User.objects.create(username=user.email, email=user.email, password=user.password,
                                   last_name=user.last_name, first_name=user.first_name)
        Client.objects.create(user=user)
        if commit:
            user.save()
        return user
