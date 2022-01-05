from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from multiselectfield import MultiSelectField
from django.db import models


JOB_CHOICES = ((1, '대학생'),
               (2, '취준생'),
               (3, '주니어 직장인'),
               (4, '시니어 직장인'))

INTEREST_CHOICES = ((1, '운동 & 건강'),
                    (2, '자격증'),
                    (3, '코딩 공부'),
                    (4, '디자인'),
                    (5, '관심분야1'),
                    (6, '관심분야2'))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, realname, phone_num, username, email_agree, sns_agree):

        user = self.model(
            email = email,
            realname = realname,
            phone_num = phone_num,
            username = username,
            email_agree = email_agree,
            sns_agree = sns_agree
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, realname=None, phone_num=None, username=None, **extra_fields):
        superuser = self.create_user(
            email = email,
            realname = realname,
            phone_num = phone_num,
            password = password,
            username = username,
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    email = models.EmailField(max_length=30, unique=True)
    realname = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=11)
    email_agree = models.BooleanField(default=False)
    sns_agree = models.BooleanField(default=False)
    username = models.CharField(max_length=20, unique=True) # 닉네임
    jobs = MultiSelectField(choices=JOB_CHOICES, max_choices=4, min_choices=0, null=True, blank=True)
    interests = MultiSelectField(choices=INTEREST_CHOICES, max_choices=6, min_choices=0, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['password', 'email', 'realname', 'phone_num', 'username', 'email_agree', 'sns_agree']

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username