from django.urls import path
from .views import QuizBoxDetail

app_name = "api"
urlpatterns = [
    path("quiz/<int:pk>/", QuizBoxDetail.as_view(), name="quizList"),
]
