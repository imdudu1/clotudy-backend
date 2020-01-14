from django.db import models
from django.utils import timezone


class ClassInformation(models.Model):
    # 강의 제목
    class_title = models.CharField(max_length=50, blank=False)
    # 담당 교수 이름
    class_advisor = models.CharField(max_length=20, blank=False)
    # 강의 소개
    class_explain = models.TextField(max_length=512)
    # 강의 종류
    class_type = models.IntegerField(default=0)
    # 생성일
    created_time = models.DateTimeField(default=timezone.now, blank=True)
    # 강의 초대 코드
    class_invite_code = models.CharField(max_length=6, default="123")

    class_pdf_path = models.CharField(max_length=50, blank=False)


class QuestionMessage(models.Model):
    # 1:N 모양을 위한 ClassInformation 와 ForeignKey 설정
    class_info = models.ForeignKey(ClassInformation, on_delete=models.CASCADE)
    # 생성일
    created_time = models.DateTimeField(default=timezone.now)
    # 질문 내용
    question_content = models.TextField(max_length=200, blank=False)
    # 공감도
    like_count = models.IntegerField(default=0)
