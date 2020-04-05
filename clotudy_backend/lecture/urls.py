from django.urls import path
from .views import *


app_name = "lecture"
urlpatterns = [
    path("<int:class_id>", view=class_detail, name="classDetail"),
    path("<int:class_id>/<int:lecture_id>", view=lecture, name="lecture"),
    path("pdf/", view=pdf_render, name="pdfViewer"),
    path("list", view=class_list, name="lectureList"),

    path("create/class", view=class_create, name="lectureCreate"),
    path("create/lecture/<int:cid>", view=lecture_create, name="lectureCreate"),
    path("create/quiz", view=quiz_create, name="lectureCreate"),
]
