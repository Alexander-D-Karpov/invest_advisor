from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.username = email
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=255, verbose_name=_("ФИО"), blank=False)
    email = models.EmailField(unique=True, blank=False)
    organization_name = models.CharField(max_length=255, blank=True)
    tax_number = models.CharField(max_length=12, verbose_name=_("ИНН"), blank=False)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=500, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    company_info = models.JSONField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "tax_number", "industry"]

    objects = UserManager()


class Company(models.Model):
    tax_number = models.CharField(max_length=12, verbose_name=_("ИНН"), blank=False)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.tax_number
