from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,first_name,last_name,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name=last_name,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    first_name       = models.CharField(max_length=100)
    last_name        = models.CharField(max_length=100)
    email            = models.EmailField(max_length=100, unique=True)
    username         = models.CharField(max_length=50, unique=True)
    contact_no       = models.CharField(max_length=20)

    #required
    date_joined      = models.DateTimeField(auto_now_add=True)
    last_login       = models.DateTimeField(auto_now=True)
    is_admin         = models.BooleanField(default=False)
    is_staff         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin    =models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    objects = MyUserManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
