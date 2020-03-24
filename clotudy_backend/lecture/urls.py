from django.urls import path
from .views import lecture, pdf_render, lecture_admin, class_list, class_detail, class_create


app_name = "lecture"
urlpatterns = [
    path("<int:class_id>", view=class_detail, name="classDetail"),
    path("<int:class_id>/<int:lecture_id>", view=lecture, name="lecture"),
    path("pdf/", view=pdf_render, name="pdfViewer"),
    path("list", view=class_list, name="lectureList"),
    path("create", view=class_create, name="lectureCreate"),
]
