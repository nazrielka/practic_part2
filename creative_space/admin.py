from django.contrib import admin
from django import forms
from .models import Client, Category, Design, Submission

admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Design)

class DesignInline(admin.StackedInline):
    model = Design
    extra = 1

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    inlines = [DesignInline]
