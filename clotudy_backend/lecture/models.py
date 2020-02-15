from django.db import models
from django.utils import timezone


class ClassInformation(models.Model):
    class_title = models.CharField(max_length=50, blank=False)
    class_instructor = models.CharField(max_length=20, blank=False)
    class_instructor_id = models.CharField(default="root", max_length=50, blank=False)
    class_description = models.TextField(max_length=512)
    class_created_time = models.DateTimeField(default=timezone.now, blank=True)
    class_invite_code = models.CharField(max_length=6, default="111111")
    class_thumbnail_path = models.CharField(max_length=100, default="")


class LectureInformation(models.Model):
    class_info = models.ForeignKey(ClassInformation, on_delete=models.CASCADE)
    lecture_title = models.CharField(max_length=50)
    lecture_description = models.TextField(max_length=128, default="")
    lecture_type = models.IntegerField(default=0)
    lecture_pdf_path = models.CharField(max_length=100, default="")
    lecture_note = models.TextField(default="")


class QuizBox(models.Model):
    lecture_info = models.ForeignKey(LectureInformation, on_delete=models.CASCADE)
    quiz_box_title = models.CharField(max_length=30)
    quiz_is_open = models.BooleanField(default=False)


class Quiz(models.Model):
    quiz_box_info = models.ForeignKey(QuizBox, on_delete=models.CASCADE)
    quiz_prob = models.TextField(max_length=512)
    # 0: choice 1: essay
    quiz_type = models.IntegerField(default=0)
    quiz_item_num = models.IntegerField(default=5)
    quiz_score = models.IntegerField(default=1)
    quiz_solve_count = models.IntegerField(default=0)
    quiz_correct_count = models.IntegerField(default=0)


class Answer(models.Model):
    quiz_info = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer_content = models.CharField(max_length=20)
    answer_choice_count = models.IntegerField(default=0)
    answer_is_correct = models.BooleanField(default=False)


class QuestionMessage(models.Model):
    lecture_info = models.ForeignKey(LectureInformation, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    user_id = models.CharField(max_length=30, default="root", blank=False)
    question_content = models.TextField(max_length=200, blank=False)
    like_count = models.IntegerField(default=0)


class QuizScoreRecord(models.Model):
    lecture_info = models.ForeignKey(LectureInformation, on_delete=models.CASCADE)
    quiz_box_info = models.ForeignKey(QuizBox, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=30, blank=False)
    score = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
