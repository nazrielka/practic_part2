from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Design
from django.core.validators import RegexValidator

cyrillic_validator = RegexValidator(
    regex=r'^[йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕННГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ -]+$',
    message='Разрешены только кириллица, дефисы и пробелы.',
)
latin_validator = RegexValidator(
    regex=r'^[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-]+$',
    message="Разрешены только латиница и дефис. Логин должен быть уникальным."
)


class ClientCreationForm(UserCreationForm):
    last_name = forms.CharField(label="Фамилия", max_length=100, validators=[cyrillic_validator])
    first_name = forms.CharField(label="Имя", max_length=100, validators=[cyrillic_validator])
    patronymic = forms.CharField(label="Отчество", max_length=100, validators=[cyrillic_validator], required=False)
    email = forms.EmailField(label="Электронная почта")
    is_agree_to_processing_data = forms.BooleanField(label="Согласие на обработку данных")
    username = forms.CharField(label="Логин", max_length=100, validators=[latin_validator])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronymic', 'email', 'is_agree_to_processing_data')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Client.objects.update_or_create(
                user=user,
                defaults={
                    'patronymic': self.cleaned_data.get('patronymic', '')
                }
            )
        return user

class DesignCreationForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['design_photo', 'comment']

    def clean(self):
        cleaned_data = super().clean()
        design_photo = cleaned_data.get('design_photo')
        comment = cleaned_data.get('comment')

        if design_photo and comment:
            raise forms.ValidationError("Заполните только одно поле: либо прикрепите готовый дизайн, либо оставьте комментарий.")
        if not design_photo and not comment:
            raise forms.ValidationError("Необходимо заполнить хотя бы одно поле: дизайн или комментарий.")

        return cleaned_data