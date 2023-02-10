from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers

def get_authenticate_user(email, password):
    user = authenticate(user=email, password=password)
    if user is None:
        raise serializers.ValidationError('Invalid username/password. Please try again!')
    return user

def create_user_account(email, password, fisrt_name='', last_name='', **extra_fields):
    user = get_user_model().objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name, **extra_fields 
    )
    return user


# Path: back-end/accounts/models.py
class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)
    
    # Method called while creating a staff user
    def create_staffuser(self, email, password, **extra_Fields):
        extra_Fields['is_staff'] = True
        extra_Fields['is_superuser'] = False

        return self.save_user(email, password, **extra_Fields)

    # Method called while calling createsuperuser
    def create_superuser(self, email, password, **extra_fields):

        #set is_superuser parameter to true
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        
        extra_fields['is_staff'] = True

        return self.save_user(email, password, **extra_fields)
 