from random import choices
import string

import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.base_user import BaseUserManager
from pytils.translit import slugify

import logging
logger = logging.getLogger(__name__)


def create_random_string(digits=False, num=4):
    if not digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должна быть указана почта")
        if not full_name:
            raise ValueError("У пользователя должно быть ФИО")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(email, full_name, password, **extra_fields)


class UserTag(models.Model):
   label = models.CharField(max_length=120,blank=False, null=True)

   def __str__(self):
       return self.label


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    slug = models.CharField('ЧПУ', max_length=255, blank=True, null=True)


    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    position = models.CharField(max_length=255, verbose_name="Должность", blank=True, null=True)
    quality = models.CharField(max_length=255, verbose_name="Квалификация", blank=True, null=True)
    photo = models.ImageField(upload_to="users/photos/", verbose_name="Фотография", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True)

    is_teacher = models.BooleanField(default=False,null=False, verbose_name="Преподаватель/Ученик")
    is_staff = models.BooleanField(default=False,null=False, verbose_name="Сотрудник")
    is_manager = models.BooleanField(default=False,null=False, verbose_name="Руководитель")

    is_active = models.BooleanField(default=True,null=False, verbose_name="Активный")
    tags = models.ManyToManyField(UserTag,blank=True)
    work_time = models.CharField(max_length=255, verbose_name="Стаж работы", blank=True, null=True)
    short_description = models.TextField(verbose_name="Короткое описание", blank=True, null=True)

    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="Почта (логин)")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class UserBiographyItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="biography_items",
        verbose_name="Пользователь"
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = "Пункт биографии"
        verbose_name_plural = "Пункты биографии"

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"


class UserFileLink(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="file_links",
        verbose_name="Пользователь"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    file = models.FileField(
        upload_to="users/files/",
        verbose_name="Файл",
        blank=True,
        null=True
    )
    link = models.URLField(verbose_name="Ссылка", blank=True, null=True)

    class Meta:
        verbose_name = "Файл или ссылка пользователя"
        verbose_name_plural = "Файлы и ссылки пользователей"

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"