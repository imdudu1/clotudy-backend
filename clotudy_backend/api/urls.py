from django.urls import path
from .views import ListClass, DetailClass, ListQuestionMessage

app_name = "api"
urlpatterns = [
    path("class/", ListClass.as_view()),
    path("class/<int:pk>/", DetailClass.as_view()),
    path("questions/", ListQuestionMessage.as_view()),
]
