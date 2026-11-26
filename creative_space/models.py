from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import Truncator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator



class Client(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    patronymic = models.CharField("Отчество", max_length=100, blank=True)
    is_agree_to_processing_data = models.BooleanField("Согласие на обработку данных", default=False)

    class Meta:
        ordering = ('user__last_name',)

    def __str__(self):
        if self.patronymic:
            return  f'{self.user.last_name} {self.user.first_name} {self.patronymic}'
        elif self.user.first_name or self.user.last_name:
            return f'{self.user.last_name} {self.user.first_name}'
        else:
            return f'{self.user.username}'

class Category(models.Model):
    name = models.CharField("Категория", max_length=50, help_text="Что требуется сделать по заявке.")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

def validate_image_size(image):
    max_size_mb = 2
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f'Размер изображения не должен превышать {max_size_mb}Мб. Пожалуйста, измените изображение.'
        )

class Submission(models.Model):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, verbose_name="Категория",on_delete=models.CASCADE, help_text="Категория заявки (что требуется сделать по заявке)")
    description = models.TextField("Описание", help_text="Предпочтения и пожелания к дизайну.")
    floor_plan=models.ImageField(
        "План помещения",
        upload_to='floor_plan/%Y/%m',
        help_text="План помещения.",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'],
                message="Допустимые форматы: JPG, JPEG, PNG, BMP.",),
            validate_image_size,],
        )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания заявки")
    WORK_STATUS = [
        ('n', 'Новый'),
        ('w', 'В работе'),
        ('r', "Выполнено"),
    ]
    status = models.CharField("Статус заявки", max_length=1, choices=WORK_STATUS, default='n')

    def __str__(self):
        short_description = Truncator(self.description).chars(30)
        if self.client and self.client.user:
            return f"{self.category.name}, {short_description} - от {self.client.user.last_name} {self.client.user.first_name} - {self.get_status_display()}"
        else:
            return f"{self.category.name}, {self.description} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse('submission-detail', args=[str(self.id)])

class Design(models.Model):
    designer = models.ForeignKey(Client, verbose_name="Дизайнер",on_delete=models.SET_NULL, null=True)
    design_photo = models.ImageField("Дизайн", upload_to='design_photos/%Y/%m', blank=True, null=True, help_text="Фотография готового дизайна (заявка получит статус 'Выполненно').")
    comment = models.TextField("Комментарий", blank=True, null=True, help_text="Введите комментарий по заявке (заявка получит статус 'В работе')")
    submission = models.OneToOneField(Submission, on_delete=models.SET_NULL, null=True, help_text="Заявка, для которой нужен дизайн.")

    def __str__(self):
        return f"Дизайн #{self.id} от {self.designer.user.last_name} {self.designer.user.first_name}"

    def save(self, *args, **kwargs):
        if self.submission:
            if self.design_photo:
                self.submission.status = 'r'
                self.submission.save()
            elif self.comment:
                self.submission.status = 'w'
                self.submission.save()
            else:
                self.submission.status = 'n'
                self.submission.save()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_or_update_user_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)