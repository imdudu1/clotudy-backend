from django.urls import path
from .views import lecture, pdf_render, lecture_admin


app_name = "lecture"
urlpatterns = [
    path("<int:class_id>/<int:lecture_id>", view=lecture, name="lecture"),
    path("admin/<int:class_id>/<int:lecture_id>", view=lecture_admin, name="lectureAdminPage"),
    path("pdf/", view=pdf_render, name="pdfViewer"),
]
