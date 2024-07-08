# django import
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# python import
from uuid import uuid4

# local import 
from .jdatetime import standard_jalali_datetime_format

# third import
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill




class AbstractUUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('ایجاد شده'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('آپدیت شده'),
    )

    class Meta:
        abstract = True

    @admin.display(description=_('ایجاد شده'), empty_value='-')
    def jcreated(self):
        return standard_jalali_datetime_format(self.created)

    jcreated.admin_order_field = 'created'

    @admin.display(description=_('آپدیت شده'), empty_value='-')
    def jupdated(self):
        return standard_jalali_datetime_format(self.updated)

    jupdated.admin_order_field = 'updated'


class AbstractStaticPage(models.Model):
    content = RichTextUploadingField(
        blank=True,
        verbose_name=_('محتوا'),
    )

    class Meta:
        abstract = True


class AbstractPageOption(models.Model):
    parallax_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='parallax/%y/%m/%d/',
        verbose_name=_('تصویر پارالاکس'),
    )
    parallax_image_thumbnail = ImageSpecField(
        source='parallax_image',
        processors=[ResizeToFill(1280, 720)],
        format='JPEG',
        options={'quality': 80}
    )

    class Meta:
        abstract = True

    @property
    def get_parallax_image(self):
        try:
            if self.parallax_image.url and self.parallax_image_thumbnail.url and self.parallax_image.file:
                image = self.parallax_image_thumbnail.url
            else:
                image = None
        except:
            image = None
        return image
