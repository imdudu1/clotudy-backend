from django.contrib import admin
from .models import *


@admin.register(QuestionMessage)
class QuestionMessageAdmin(admin.ModelAdmin):
    list_display = ['lecture_info', 'created_time', 'like_count']


@admin.register(ClassInformation)
class ClassInformationAdmin(admin.ModelAdmin):
    list_display = ['class_title', 'class_instructor', 'class_description']


@admin.register(LectureInformation)
class LectureInformationAdmin(admin.ModelAdmin):
    list_display = ['lecture_title']


@admin.register(QuizBox)
class QuizBoxAdmin(admin.ModelAdmin):
    list_display = ['quiz_box_title']


@admin.register(Quiz)
class Quiz(admin.ModelAdmin):
    list_display = ['quiz_prob', 'quiz_score', 'quiz_solve_count']


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = ['answer_content', 'answer_choice_count', 'answer_is_correct']


@admin.register(QuizScoreRecord)
class QuizScoreRecord(admin.ModelAdmin):
    list_display = ['user_id', 'score', 'created_date']


@admin.register(QuizBoxLink)
class QuizBoxLink(admin.ModelAdmin):
    list_display = ['lecture_info', 'quiz_box']
