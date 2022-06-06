from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    def is_admin(self):
        return Administrator.objects.filter(user=self.id)


class Administrator(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, db_column='User ID', verbose_name='User')

    class Meta:
        unique_together = ('id', 'user')

    def __str__(self):
        return self.user.username


class Employee(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, db_column='UserID', verbose_name='User')

    class Meta:
        unique_together = ('id', 'user')

    def get_user(self):
        return self.user.username


class Client(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, db_column='UserID', verbose_name='User')
    nif = models.IntegerField(db_column='NIF', verbose_name='NIF', null=True)

    class Meta:
        unique_together = ('id', 'user')

    def __str__(self):
        return self.user.username


class Car(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    client = models.ForeignKey(Client, models.CASCADE, db_column='ClientID', verbose_name='Client')
    registration = models.CharField(db_column='Registration', verbose_name='Registration', unique=True, max_length=8)
    foreign = models.BooleanField(db_column='Is Foreign', verbose_name='Is Foreign', unique=True)
    brand = models.CharField(db_column='Brand', verbose_name='Brand', unique=True, max_length=20)
    model = models.CharField(db_column='Model', verbose_name='Model', unique=True, max_length=20)

    def __str__(self):
        return self.registration


class Notification(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='UserID', verbose_name='User')
    title = models.CharField(db_column='Title', verbose_name='Title', unique=True, max_length=30)
    seen = models.BooleanField(db_column='MessageSeen', verbose_name='Message Seen', default=False)
    description = models.TextField(db_column='Description', verbose_name='Description')
