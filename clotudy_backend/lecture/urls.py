from django.urls import path
from .views import lecture


app_name = "lecture"
urlpatterns = [
    path("<int:room_id>/", view=lecture, name="view_lecture"),
]
