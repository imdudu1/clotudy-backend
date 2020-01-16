from django.urls import path
from .views import lecture, pdf_render, lecture_admin


app_name = "lecture"
urlpatterns = [
    path("<int:room_id>/", view=lecture, name="lecture"),
    path("pdf/", view=pdf_render, name="pdfViewer"),

    path("admin/<int:room_id>", view=lecture_admin, name="lectureAdminPage"),
]
