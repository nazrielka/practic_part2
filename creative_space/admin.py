from django.contrib import admin
from django import forms
from .models import Client, Category, Design, Submission

admin.site.register(Client)
admin.site.register(Category)

class DesignInline(admin.TabularInline):
    model = Design
    extra = 1


class DesignAdminForm(forms.ModelForm):
    submission_status = forms.ChoiceField(choices=Submission.WORK_STATUS,
    label='Статус заявки',
    required=False,)

    class Meta:
        model = Design
        fields = '__all__'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    inlines = [DesignInline]

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    form = DesignAdminForm