from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, realname):

        if not username:
            raise ValueError('must have username')
        if not realname:
            raise ValueError('must have realname')

        user = self.model(
            username=username,
            realname=realname,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, realname, password):

        user = self.create_user(
            username=username,
            realname=realname
        )
        user.set_password(password)
        user.is_staff = True  # 슈퍼유저 권한 부여
        user.is_superuser = True  # 슈퍼유저 권한 부여
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(
        max_length=50,
        unique=True
    )
    realname = models.CharField(
        max_length=20
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['realname', ]

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser