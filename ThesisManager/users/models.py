from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here. 

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, account_type=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        
        user = self.model(username=username, account_type=account_type, **extra_fields)

        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, account_type=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        
        user = self.model(username=username, account_type=account_type, **extra_fields)
        
        if password:
            user.set_password(password)
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
        
class CustomUser(AbstractBaseUser,PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = (
        ('unit coordinator', 'Unit Coordinator'),
        ('supervisor', 'Supervisor'),
        ('student', 'Student'),
        ('admin', 'Admin')
    )
    
    username = models.CharField(max_length=20, unique=True, default='')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['account_type']
    
    def __str__(self):
        return self.username
