from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from multiselectfield import MultiSelectField
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, realname, phone_num, nickname):

        user = self.model(
            email = email,
            realname = realname,
            phone_num = phone_num,
            nickname = nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, nickname=None, **extra_fields):
        superuser = self.create_user(
            email = email,
            password = password,
            nickname = nickname,
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    email = models.EmailField(max_length=30)
    realname = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=11)
    auth_num =  models.CharField(max_length=10, null=True, blank=True)
    email_agree = models.BooleanField(default=False)
    sns_agree = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20)
    # jobs =
    # interests =
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['password', 'email', 'realname', 'phone_num', 'nickname']

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.nickname