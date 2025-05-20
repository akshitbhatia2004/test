from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission , AbstractUser , User
from django.conf import settings  # ✅ import this

# --------------------------
# Custom User Manager
# --------------------------
class ParentSignupManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

# --------------------------
# Custom User Model
# --------------------------
class ParentSignup(AbstractBaseUser, PermissionsMixin):
    parent_name = models.CharField(max_length=100)
    child_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='parent_signup_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='parent_signup_permissions',
        blank=True
    )

    objects = ParentSignupManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'parent_name', 'mobile']

    def __str__(self):
        return self.username

# --------------------------
# Other Models (no change)
# --------------------------


# Evaluator


class Evaluator(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)


# Parent

class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    child_name = models.CharField(max_length=100)
    child_dob = models.DateField()

# Assessment

class Assessment(models.Model):
    child_id = models.IntegerField()
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Assessment {self.id} - Score: {self.score}"

# Institute Signup

class InstituteSignup(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()


    

class CustomUser(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('institute', 'Institute'),
        ('evaluator', 'Evaluator'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    
    
# profile

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

