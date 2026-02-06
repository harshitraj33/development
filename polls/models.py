from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password, identify_hasher


# Create your models here.
class users (models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

class FormModel(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()
    # last_modified = models.DateTimeField(auto_now_add = True)
    # img = models.ImageField(upload_to = "images/")

    def __str__(self):
        return self.title
    
class LoginUser(models.Model):
    
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username

class SignupUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
        login_user, _ = LoginUser.objects.get_or_create(username=self.username)
        login_user.password = self.password
        login_user.is_active = self.is_active
        login_user.save()

    def __str__(self):
        return self.username

        
    
