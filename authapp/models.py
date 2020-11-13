from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):

    # create_user and create_superuser is mandatory

    def create_user(self, email, username, phone, first_name, password=None):
        if not email:
            raise ValueError("email Required!")
        if not username:
            raise ValueError("Username required!")
        if not phone:
            raise ValueError("Phone number required!")
        if not first_name:
            raise ValueError("First Name required!")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, first_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
            first_name=first_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(max_length=60, unique=True)
    phone = models.IntegerField()
    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # values will be identified using email now
    # shouldn't add 'username' here, since it is already in USERNAME_FIELD
    REQUIRED_FIELDS = ['email', 'phone', 'first_name']

    objects = MyAccountManager()

    # these 3 are required methods
    def __str__(self):  # This gets displayed when an object of Account class is called in template
        return self.email + ", " + self.username  # multiple values can be concatinated like this

    def has_perm(self, perm, obj=None):  # has permission to make changes
        return self.is_admin  # only allowed if admin

    def has_module_perms(self, app_label):  # give permission to module
        return True  # instead of True we can give access to specific position (eg: is_admin, is_staff or both)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
