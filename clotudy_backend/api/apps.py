from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiConfig(AppConfig):
    name = 'clotudy_backend.api'
    verbose_name = _("Api")

    def ready(self):
        try:
            import clotudy_backend.api.signals  # noqa F401
        except ImportError:
            pass
