from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users mush have an email address')
        # normalize_email is a helper function thay comes with BaseUserManager
        # this is a bit confusing to me: self.model
        # self.model is an attribute that Django sets into the manager
        # instance to get the model class to which they're attached
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # optional; database specific

        return user

    # since create_superuse is only in the command line, there is no need
    # for **extra_fields
    def create_superuser(self, email, password=None):
        """ Creates and saves a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # what is this for?
    USERNAME_FIELD = 'email'