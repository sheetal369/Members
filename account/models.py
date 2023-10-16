from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account import commons
from tinymce.models import HTMLField


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    is_email_verified=models.BooleanField(default=True)
    otp=models.CharField(max_length=200,null=True,blank=True)
    is_otp_verified=models.BooleanField(default=True)
    organization_name = models.CharField(max_length=255,null=True,blank=True)
    first_name = models.CharField(max_length=30,null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    subdomain = models.CharField(max_length=50, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['organization_name','first_name','last_name','phone_number','subdomain']
    role = models.CharField(max_length=20, choices=commons.USER_ROLES)

    def __str__(self):
        return self.email

class Membership(models.Model):
    membership_name=models.CharField(max_length=225)
    first_time_charge=models.IntegerField()
    recurring_charge=models.IntegerField()
    renewal_period=models.IntegerField()
    amount=models.IntegerField()
    
class Manager(models.Model):
    first_name=models.CharField(max_length=225)
    last_name=models.CharField(max_length=225)
    email=models.CharField(max_length=225)
    contact=models.CharField(max_length=225)
    
class Member(models.Model):
    first_name=models.CharField(max_length=225)
    last_name=models.CharField(max_length=225)
    email=models.EmailField()
    contact=models.CharField(max_length=225)
    
    old_member=models.BooleanField()
    member_id=models.CharField(max_length=225)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    enrolled_membership=models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="member")

    
class Event(models.Model):
    event_name=models.CharField(max_length=225)
    venue=models.CharField(max_length=225)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    image=models.ImageField()
    short_description=HTMLField()
    long_description=HTMLField()
    allow_registration = models.BooleanField()

class TicketType(models.Model):
    class currency_type(models.TextChoices):
        USD="USD"
        NPR="Nepalese Rupees"
    
    ticket_name=models.CharField(max_length=225)
    currency=models.CharField(max_length=225,choices=currency_type.choices, default=currency_type.NPR)
    ticket_price=models.IntegerField()
    ticket_description=models.CharField(max_length=225)
    registration_limit=models.IntegerField()
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_type")

class Registration(models.Model):
    allow_registration=models.BooleanField()
    available_from=models.DateTimeField()
    available_to=models.DateTimeField()
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registration")