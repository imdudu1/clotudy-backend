from django.urls import path
from .views import *

app_name = "api"
urlpatterns = [
    path("quiz", QuizBoxList.as_view(), name="quizBoxList"),
    path("quiz/<int:class_pk>/<int:lecture_pk>", QuizBoxDetail.as_view(), name="quizDetail"),
    path("ppthistory/<int:pk>", PPTTimeHistory.as_view(), name="pptTime"),
    path("bonus/<int:class_pk>/<int:lecture_pk>", StudentBonusPoin.as_view(), name="bonus"),
]
