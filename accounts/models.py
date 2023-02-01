from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.utils import UserManager

class Location(models.Model):
    county = models.CharField(max_length=80)
    sub_county = models.CharField(max_length=80)
    constituency = models.CharField(max_length=80)


class UserProfile(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    bio = models.TextField()
    phone_number = models.CharField(max_length=10, default='07XXXXXXX')
    national_id = models.PositiveBigIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='accounts/user/avatar/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    def get_avatar_url(self) -> str: # image url
        return self.avatar.url
    

    class Meta:
        db_table = 'user_profiles'
