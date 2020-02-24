from django.urls import path
from .views import QuizBoxDetail, PPTTimeHistory

app_name = "api"
urlpatterns = [
    path("quiz/<int:pk>", QuizBoxDetail.as_view(), name="quizList"),
    path("ppthistory/<int:pk>", PPTTimeHistory.as_view(), name="pptTime"),
]
