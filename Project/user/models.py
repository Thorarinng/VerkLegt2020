from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create User
from django.db.models import Model


class UserManager(BaseUserManager):
    def createUser(self):
        pass

    def createStaffUser(self):
        pass

# User
class User(AbstractBaseUser):
    # In AbstractBaseUser : id, password, last_login
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=20, null=False, blank=True)
    imgURL = models.CharField(max_length=999, blank=True)
    active = models.BooleanField(default=True)
    employee = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [firstName, lastName, email]

    object = UserManager()

    def __str__(self):
        return self.email

    @property
    def getFullName(self):
        return self.firstName + " " + self.lastName

    @property
    def getPhoneNumber(self):
        return self.phoneNumber

    @property
    def getImgURL(self):
        return self.imgURL

    @property
    def isAdmin(self):
        return self.admin

    @property
    def isEmployee(self):
        return self.employee

    @property
    def isActive(self):
        return self.active

