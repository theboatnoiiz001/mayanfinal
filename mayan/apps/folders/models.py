from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document


@python_2_unicode_compatible
class Folder(models.Model):
    title = models.CharField(max_length=128, verbose_name=_('Title'), db_index=True)
    user = models.ForeignKey(User, verbose_name=_('User'))
    datetime_created = models.DateTimeField(verbose_name=_('Datetime created'), auto_now_add=True)
    documents = models.ManyToManyField(Document, related_name='folders', verbose_name=_('Documents'))

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('folders:folder_view', [self.pk])

    class Meta:
        unique_together = ('title', 'user')
        ordering = ('title',)
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')
