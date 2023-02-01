from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

class Gender(models.TextChoices):
    MALE = (
        "MALE",
        _("male"),
    )
    FEMALE = (
        "FEMALE",
        _("Female"),
    )
    OTHER = "OTHER", _("Other")

class LanguageEnum(models.TextChoices):
    
    ENGLISH = ("EN",
    _("english"),
    )
    
    SPANISH = (
        "ES",
    _("Espanol"),
    )

    DUTCH = (
        "NL",
    _("nederlands")
    )    

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_nr = models.CharField(max_length=15)
    password = models.CharField(max_length=64)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    spoken_languages = models.CharField(max_length=255, choices=LanguageEnum.choices, default = LanguageEnum.ENGLISH)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'email']

    def __str__(self):
        return self.email
