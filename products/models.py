from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)


class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=150)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True)
    address = models.CharField(max_length=155, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=255, null=True)
    postal_code = models.IntegerField(null=True)
    country = models.CharField(max_length=170, null=True)
    is_active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True)
    description = models.TextField(null=True)
    sku = models.CharField(max_length=50, unique=True, null=True)
    upc = models.CharField(max_length=50, unique=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True)
    updated_date = models.DateTimeField(default=timezone.now)
    weight = models.IntegerField(null=True)
    dimensions = models.CharField(null=True)
    color = models.CharField(null=True, blank=True)
    size = models.CharField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/')
