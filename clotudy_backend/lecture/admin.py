from django.contrib import admin
from .models import QuestionMessage, ClassInformation


@admin.register(QuestionMessage)
class QuestionMessageAdmin(admin.ModelAdmin):
    list_display = ['class_info', 'created_time', 'like_count']


@admin.register(ClassInformation)
class ClassInformationAdmin(admin.ModelAdmin):
    list_display = ['class_title', 'class_advisor', 'class_type']