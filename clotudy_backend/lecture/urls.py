from django.urls import path
from .views import lecture, pdf_render, test_admin


app_name = "lecture"
urlpatterns = [
    path("<int:room_id>/", view=lecture, name="view_lecture"),
    path("pdf/", view=pdf_render, name="pdf_render"),
]
