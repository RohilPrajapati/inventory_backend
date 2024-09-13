from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.BooleanField()

    def __str__(self) -> str:
        return self.name

class User(AbstractUser):
    username = models.CharField(unique=True)
    email = models.EmailField(_("email address"), unique=True)
    role = models.OneToOneField(Role,on_delete=models.PROTECT,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Permissions(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(null=True, blank=True)


class RolePermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    permission = models.ForeignKey(Permissions, on_delete=models.PROTECT)

