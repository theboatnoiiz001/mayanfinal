import bleach

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import event_theme_created, event_theme_edited

FONT_CHOICES = (
    ('Kanit','Kanit font'),
    ('Roboto', 'Roboto font'),
    ('Prompt','Prompt font'),
)

class Theme(ExtraDataModelMixin, models.Model):
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the theme.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
    stylesheet = models.TextField(
        blank=True, help_text=_(
            'The CSS stylesheet to change the appearance of the different '
            'user interface elements.'
        ), verbose_name=_('Stylesheet')
    )
    brand_name = models.CharField(
        blank=True,
        max_length=100,
        help_text=_(
            'Set text Brand.'
        ),
        verbose_name=_('Brand name')
    )
    logo_path = models.TextField(
        blank=True,
        verbose_name=_('Path logo')
    )
    font = models.CharField(
        max_length=100,
        blank=True,
        choices=FONT_CHOICES,
        verbose_name=_('Font')
    )
    color_font_header = RGBColorField(
        blank=True,
        help_text=_('Color font header.'),
        verbose_name=_('Color font header')
    )
    background_color_header = RGBColorField(
        blank=True,
        help_text=_('Color background header.'),
        verbose_name=_('Color background header')
    )
    background_color_menu = RGBColorField(
        blank=True,
        help_text=_('Color background menu.'),
        verbose_name=_('Color background menu')
    )
    background_color_header_panel = RGBColorField(
        blank=True,
        help_text=_('Color background header panel.'),
        verbose_name=_('Color background header panel')
    )
    background_website = RGBColorField(
        blank=True,
        help_text=_('Color background website.'),
        verbose_name=_('Color background website')
    )
    font_other = models.CharField(
        blank=True,
        max_length=300,
        help_text=_(
            'Name font from Google Font.'
        ),
        verbose_name=_('Font other')
    )
    background_menu_dropdown = RGBColorField(
        blank=True,
        help_text=_('Color background dropdown menu.'),
        verbose_name=_('Color background dropdown menu')
    )
    btn_color_primary = RGBColorField(
        blank=True,
        help_text=_('Color primary button.'),
        verbose_name=_('Color primary button')
    )
    btn_color_danger = RGBColorField(
        blank=True,
        help_text=_('Color danger button.'),
        verbose_name=_('Color danger button')
    )
    btn_color_success = RGBColorField(
        blank=True,
        help_text=_('Color success button.'),
        verbose_name=_('Color success button')
    )
    btn_color_default = RGBColorField(
        blank=True,
        help_text=_('Color default button.'),
        verbose_name=_('Color default button')
    )
    font_size_header = models.IntegerField(
        default=19,
        help_text=_(
            'Font size header brand.'
        ),
        verbose_name=_('Font size brand')
    )
    font_size_menu = models.IntegerField(
        default=15,
        help_text=_(
            'Font size menu.'
        ),
        verbose_name=_('Font size menu')
    )
    font_size_content_title = models.IntegerField(
        default=23,
        help_text=_(
            'Font size content title.'
        ),
        verbose_name=_('Font size content title')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')

    def __str__(self):
        return force_text(s=self.label)

    def get_absolute_url(self):
        return reverse(
            viewname='appearance:theme_edit', kwargs={
                'theme_id': self.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_theme_created,
            'target': 'self',
        },
        edited={
            'event': event_theme_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        self.stylesheet = bleach.clean(
            text=self.stylesheet, tags=('style',)
        )
        super().save(*args, **kwargs)


class UserThemeSetting(models.Model):
    user = models.OneToOneField(
        on_delete=models.CASCADE, related_name='theme_settings',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    theme = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_setting', to=Theme, verbose_name=_('Theme')
    )

    class Meta:
        verbose_name = _('User theme setting')
        verbose_name_plural = _('User theme settings')

    def __str__(self):
        return force_text(s=self.user)
