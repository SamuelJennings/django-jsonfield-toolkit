from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JSONFieldExtrasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jsonfield_toolkit"
    verbose_name = _("JSON Field Extras")
