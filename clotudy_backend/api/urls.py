from django.urls import path
from .views import QuizBoxDetail, PPTTimeHistory
from django.views.decorators.csrf import csrf_exempt

app_name = "api"
urlpatterns = [
    path("quiz/<int:pk>", QuizBoxDetail.as_view(), name="quizList"),
    path("ppthistory/<int:pk>", csrf_exempt(PPTTimeHistory.as_view()), name="pptTime"),
]
