from django.db import models
from django.contrib.auth.models import User
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, address, phone, id, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not id:
            raise ValueError('Users must have an id')

        user = self.model(
            email=self.normalize_email(email),
            address=address,
            phone=phone,
            id=id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    address = models.TextField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(null=True, blank=True)
    isFacility=models.BooleanField(default=True,null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    


class Patient(MyUser):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.first_name + " " + self.first_name


class Facility(MyUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    Description = models.TextField(max_length=500, null=True, blank=True)
    categories = models.TextField(max_length=500, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    ratting = models.FloatField(null=True, blank=True)
    Patients = models.ManyToManyField("Patient", null=True, blank=True)

    def __str__(self):
        return self.name
