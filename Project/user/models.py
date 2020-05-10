# Django libraries
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Model

# Third-party libraries
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django_countries.fields import CountryField


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

    def __setUserAttributes__(self, form):
        self.firstName = form.cleaned_data['firstName']
        self.lastName = form.cleaned_data['lastName']
        self.phoneNumber = form.cleaned_data['phoneNumber']
        self.imgURL = form.cleaned_data['imgURL']
        self.set_password(form.cleaned_data['password'])

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
    # country = models.CharField(max_length=100)
    # Added this third party django-countries library that allows us to use a selector field for countries
    country = CountryField()
    region = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Sets attributes to a shippingAddress object and returns it
    def setShippingAddressAttributes(self, request, form):
        self.user_id = request.user.pk
        self.address1 = form.cleaned_data.get('address1')
        self.address2 = form.cleaned_data.get('address2')
        self.city = form.cleaned_data.get('city')
        self.country = form.cleaned_data.get('country')
        self.region = form.cleaned_data.get('region')
        self.postalCode = form.cleaned_data.get('postalCode')
        return self

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


class PaymentMethod(models.Model):
    # # pip install django-credit-cards
    # nameOnCard = models.CharField(max_length=255)
    # # Only stores 4 bytes by default
    # cardNumber = models.PositiveIntegerField(max_length=16)
    # expMonth = models.CharField(max_length=2)
    # expYear = models.CharField(max_length=4)
    # cvc = models.IntegerField()

    nameOnCard = models.CharField(max_length=255)
    cardNumber = CardNumberField(max_length=16)
    cardExpiry = CardExpiryField(max_length=4)
    cvc = SecurityCodeField('security code')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def setPaymentMethodAttributes(self, request, form):
    #     self.user_id = request.user.pk
    #     self.nameOnCard = form.cleaned_data.get('nameOnCard')
    #     self.cardNumber = form.cleaned_data.get('cardNumber')
    #     self.expMonth = form.cleaned_data.get('expMonth')
    #     self.expYear = form.cleaned_data.get('expYear')
    #     self.cvc = form.cleaned_data.get('cvc')
    #     return self
    #
    # def validateAttributes(self, request, form):
    #     if len(form.cleaned_data.get('nameOnCard')) != 16:
    #         return False