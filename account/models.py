# Django Built-in modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel, AbstractUUIDModel
from .managers import UserManager


# Python Standard Library
import uuid as _uuid

# Third Party Packages
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(AbstractBaseUser, AbstractDateTimeModel, AbstractUUIDModel, PermissionsMixin):
    """
    This models inherits from django base user.
    """
    uuid = models.UUIDField(unique=True, default=_uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('نام کاربری'),
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name=_('نام'),
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('نام خانوادگی'),
    )
    mobile_number = PhoneNumberField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('شماره موبایل'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    avatar = models.ImageField(
        upload_to='users/avatar/%y/%m/%d',
        null=True,
        blank=True,
        verbose_name=_('تصویر پروفایل'),
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(250, 250)],
        format='PNG',
        options={'quality': 70}
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال'),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_('ادمین'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('کارمند'),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name', 'last_name',)
    objects = UserManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def __str__(self):
        return self.username

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def get_avatar(self):
        try:
            if self.avatar.url and self.avatar_thumbnail.url and self.avatar.file:
                image = self.avatar_thumbnail.url
        except:
            image = settings.DEFAULT_AVATAR_PATH
        return image

    def is_admin(self):
        return self.is_authenticated and self.is_superuser and self.is_staff


class MobilePhoneVerify(AbstractDateTimeModel):
    USABLE = 0
    USELESS = 1
    STATUS_CHOICE = (
        (USABLE, _('قابل استفاده')),
        (USELESS, _('غیر قابل استفاده')),
    )
    mobile_number = PhoneNumberField(
        unique=True,
        verbose_name=_('شماره موبایل'),
    )
    code = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('کد'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICE,
        default=USABLE,
        verbose_name=_('وضعیت'),
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('کد تایید')
        verbose_name_plural = _('کد های تایید')

    def __str__(self):
        return str(self.mobile_number)


class Bookmark(AbstractDateTimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('کاربر')
    )
    post = models.ForeignKey(
        "blog.Post",
        on_delete=models.CASCADE,
        verbose_name=_('پست')
    )

    class Meta:
        verbose_name = _('لیست مطالعه')
        verbose_name_plural = _("لیست های مطالعه")


class Profile(AbstractDateTimeModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('کاربر'),
    )
    slug = models.SlugField(
        allow_unicode=True,
        unique=True,
        verbose_name=_('اسلاگ'),
    )
    bio = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('بیوگرافی'),
    )
    display_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('اسم نمایشی'),
    )
    position = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('سمت'),
    )

    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل')
        ordering = ('-created',)

    def __str__(self):
        return self.get_display_name

    def get_absolute_url(self):
        return reverse('author_profile', args=[self.slug])

    @property
    def get_display_name(self):
        return self.display_name if self.display_name else self.user.fullname
