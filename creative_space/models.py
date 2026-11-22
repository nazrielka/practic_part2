from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from django.conf import settings
from datetime import date

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    patronimic = models.CharField(max_length=100, blank=True, help_text='Введите отчество')

    class Meta:
        ordering = ('user__last_name',)

    def __str__(self):
        return self.user.username

class Disign(models.Model):
    disigner = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    disign_photo = models.ImageField(upload_to='disign_photos/%Y/%m', blank=True, null=True, help_text="Фотография готового дизайна.")
    comment = models.TextField(blank=True, null=True, help_text="Введите комментарий по заявке.")

    class Meta:
        ordering = ('disigner',)

    def __str__(self):
        return f"Дизайн #{self.id}"

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Submission(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    disign = models.ForeignKey(Disign, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, blank=True, null=True, help_text="Для чего и какой дизайн вам нужен.")
    description = models.TextField(blank=True, null=True, help_text="Предпочтения и пожелания к дизайну.")
    floor_plan = models.ImageField(upload_to='floor_plan/%Y/%m', blank=True, null=True, help_text="План помещения.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания заявки")
    WORK_STATUS = [
        ('n', 'Новый'),
        ('w', 'В работе'),
        ('r', "Выполнено"),
    ]
    status = models.CharField(max_length=1, choices=WORK_STATUS, default='n', help_text="Статус заявки.")