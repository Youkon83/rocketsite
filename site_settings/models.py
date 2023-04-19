from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField


@register_setting
class ContactSettings(BaseSetting):

    contact = RichTextField(
        blank=True,
        null=True,
        )
    
    panels = [
        FieldPanel("contact")
    ]

@register_setting
class HoursSettings(BaseSetting):

    hours = RichTextField(
        blank=True,
        null=True,
        )
    
    panels = [
        FieldPanel("hours")
    ]
