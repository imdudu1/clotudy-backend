from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LectureConfig(AppConfig):
    name = 'clotudy_backend.lecture'
    verbose_name = _("Lecture")

    def ready(self):
        try:
            import clotudy_backend.lecture.signals
        except ImportError:
            pass
