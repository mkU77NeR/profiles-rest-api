from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email adress')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password) # encrypt password
        user.save(using=self._db) # standard for saving object in django
        
        return user
    
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        
        user = self.create_user(email, name, password)
        
        user.is_superuser = True #from PermissionsMixin
        user.is_staff = True        
        user.save(using=self._db)
        
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    # we want a email column on our user profile database table
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self) -> str:
        """Return string representation of our user"""
        return self.email
    
