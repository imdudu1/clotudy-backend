from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CloredisConfig(AppConfig):
    name = 'clotudy_backend.cloredis'
    verbose_name = _("Cloredis")

    def ready(self):
        try:
            import clotudy_backend.cloredis.signals
        except ImportError:
            pass
