from multiselectfield import MultiSelectField
from django.db import models
from accounts.util import choices
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, realname, username, email_agree, sns_agree):

        user = self.model(
            email=email,
            realname=realname,
            username=username,
            email_agree=email_agree,
            sns_agree=sns_agree
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, realname=None, username=None, email_agree=None, sns_agree=None):
        superuser = self.create_user(
            email=email,
            realname=realname,
            password=password,
            username=username,
            email_agree=email_agree,
            sns_agree=sns_agree
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=30, unique=True)
    realname = models.CharField(max_length=30)
    email_agree = models.BooleanField(default=False)
    sns_agree = models.BooleanField(default=False)
    username = models.CharField(max_length=20, unique=True)  # 닉네임
    jobs = MultiSelectField(choices=choices.JOB_CHOICES, max_choices=4, min_choices=0, null=True, blank=True)
    interests = MultiSelectField(choices=choices.INTEREST_CHOICES, max_choices=6, min_choices=0, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'realname', 'username', 'email_agree', 'sns_agree']

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser