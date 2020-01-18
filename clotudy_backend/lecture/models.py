from django.db import models
from django.utils import timezone


class ClassInformation(models.Model):
    # 강의 제목
    class_title = models.CharField(max_length=50, blank=False)
    # 담당 교수 이름
    class_instructor = models.CharField(max_length=20, blank=False)
    # 강의 소개
    class_description = models.TextField(max_length=512)
    # 생성일
    class_created_time = models.DateTimeField(default=timezone.now, blank=True)
    # 강의 초대 코드
    class_invite_code = models.CharField(max_length=6, default="111111")


class LectureInformation(models.Model):
    class_info = models.ForeignKey(ClassInformation, on_delete=models.CASCADE)
    lecture_title = models.CharField(max_length=50)
    lecture_type = models.IntegerField(default=0)
    lecture_rsrc_path = models.CharField(max_length=256)


class QuizBox(models.Model):
    lecture_info = models.ForeignKey(LectureInformation, on_delete=models.CASCADE)
    quiz_box_title = models.CharField(max_length=30)


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
    # 1:N 모양을 위한 ClassInformation 와 ForeignKey 설정
    class_info = models.ForeignKey(LectureInformation, on_delete=models.CASCADE)
    # 생성일
    created_time = models.DateTimeField(default=timezone.now)
    # 질문 내용
    question_content = models.TextField(max_length=200, blank=False)
    # 공감도
    like_count = models.IntegerField(default=0)
