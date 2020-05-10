from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create User
from django.db.models import Model


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


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

    objects = UserManager()

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

class ShippingAddress(models.Model):
    address1 = models.CharField(max_length=80)
    address2 = models.CharField(max_length=80)
    city = models.CharField(max_length=100, default=None)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def getAddress1(self):
        return self.address1

    @property
    def getAddress2(self):
        return self.address2

    @property
    def getCity(self):
        return self.city

    @property
    def getCountry(self):
        return self.country

    @property
    def getRegion(self):
        return self.region

    @property
    def getPostalCode(self):
        return self.postalCode

    @property
    def getUser(self):
        return self.user

    def __str__(self):
        return f"{self.pk}\n" \
               f"{self.address1}\n" \
               f"{self.address2}\n" \
               f"{self.city}\n" \
               f"{self.country}\n" \
               f"{self.region}\n" \
               f"{self.postalCode}\n" \
               f"{self.user}\n"


