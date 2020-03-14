from django.urls import path
from .views import QuizBoxDetail, PPTTimeHistory, BonusPoint

app_name = "api"
urlpatterns = [
    path("quiz/<int:class_pk>/<int:lecture_pk>", QuizBoxDetail.as_view(), name="quizList"),
    path("ppthistory/<int:pk>", PPTTimeHistory.as_view(), name="pptTime"),
    path("bonus/<int:class_pk>/<int:lecture_pk>", BonusPoint.as_view(), name="bonus"),
]
