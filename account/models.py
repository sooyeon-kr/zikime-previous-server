
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    """Custom User Model"""
    
    TYPE_PROTECTOR = "protector"
    TYPE_PROTEGE = "protege"
    TYPE_OTHER = "other"
    TYPE_CHOICES = (
        (TYPE_PROTECTOR, "Protector"),
        (TYPE_PROTEGE, "Protege"),
        (TYPE_OTHER, "Other"),
    )

    type = models.CharField(
        choices=TYPE_CHOICES, max_length=10, null=True, blank=True
    )

