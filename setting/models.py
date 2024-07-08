# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from colorfield.fields import ColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class SiteGlobalSetting(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام وبسایت'),
    )
    slogan = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('شعار'),
    )
    about = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('توضیحات فوتر'),
    )
    copyright = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('متن کپی رایت'),
    )
    logo = models.ImageField(
        upload_to='site/',
        null=True,
        blank=True,
        verbose_name=_('لوگو'),
    )
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors=[ResizeToFill(250, 250)],
        format='PNG',
        options={'quality': 80}
    )
    favicon = models.ImageField(
        upload_to='site/',
        null=True,
        blank=True,
        verbose_name=_('فاوآیکون'),
    )
    favicon_thumbnail = ImageSpecField(
        source='favicon',
        processors=[ResizeToFill(180, 180)],
        format='PNG',
        options={'quality': 80}
    )
    main_banner = models.ImageField(
        upload_to='site/',
        null=True,
        blank=True,
        verbose_name=_('بنر اصلی'),
    )
    main_banner_link = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('لینک بنر اصلی'),
        help_text=_('سایز پیشنهادی برای ارتفاع بنر حداکثر ۲۵۰ و طول آن حداکثر ۱۴۴۰ می باشد.'),
    )
    fax = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('فکس'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    video = models.FileField(
        _('فیلم معرفی'),
        upload_to='site/',
        null=True,
        blank=True,
        )

    class Meta:
        verbose_name = _('پیکربندی سایت')
        verbose_name_plural = _("پیکربندی سایت")

    def __str__(self):
        return str(_('پیکربندی سایت'))

    @property
    def default_search_engine_title(self):
        return self.__str__()

    @property
    def get_logo(self):
        if self.logo and self.logo.file:
            print(self.logo)
            return self.logo_thumbnail.url

    @property
    def get_favicon(self):
        if self.favicon and self.favicon.file:
            return self.favicon_thumbnail.url

    def have_contact_ways(self):
        return self.phone or self.email


class Address(AbstractDateTimeModel):
    site = models.ForeignKey(
        SiteGlobalSetting,
        on_delete=models.CASCADE,
        verbose_name=_('سایت'),
        related_name='addresses'
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('عنوان')
    )
    address = models.TextField(
        verbose_name=_('آدرس'),
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('شماره تلفن')
    )
    time = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('ساعات کاری')
    )
    map = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('نقشه'),
        help_text=_('کد html نقشه را وارد کنید'),
    )



    class Meta:
        verbose_name = _('آدرس')
        verbose_name_plural = _('آدرس ها')

    def __str__(self):
        return self.address
    
    
class PhoneNumber(AbstractDateTimeModel):
    site = models.ForeignKey(
        SiteGlobalSetting,
        on_delete=models.CASCADE,
        verbose_name=_('سایت')
    )
    phone = models.CharField(
        max_length=255,
        verbose_name=_('شماره تلفن')
    )

    

    class Meta:
        verbose_name = _('شماره تلفن')
        verbose_name_plural = _('شماره تلفن ها')

    def __str__(self):
        return self.phone


class SocialMediaSetting(AbstractDateTimeModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_('نام'),
    )
    # username_or_id = models.CharField(
    #     max_length=100,
    #     verbose_name=_('نام کاربری یا آیدی'),
    #     help_text=_('مثال: firefly@'),
    # )
    # icon = models.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    #     help_text=_(
    #         'به صورت پیشفرض از fontawesome پشتیبانی می شود، فقط کافیست نام آیکون را وارد کنید. برای مثال: facebook'
    #     ),
    #     verbose_name=_('آیکون'),
    # )
    icon = models.FileField(
        _("آیکون"), 
        upload_to='socials/logo/%y/%m/%d'
    )
    # icon_background_color = ColorField(
    #     null=True,
    #     blank=True,
    #     default='#FF0000',
    #     verbose_name=_('رنگ پس زمینه آیکون'),
    # )
    link = models.URLField(
        verbose_name=_('لینک'),
    )

    class Meta:
        verbose_name = _('شبکه اجتماعی')
        verbose_name_plural = _("شبکه های اجتماعی")

    def __str__(self):
        return self.name


class HomePageSlider(AbstractDateTimeModel):

    site = models.ForeignKey(
        SiteGlobalSetting,
        on_delete=models.CASCADE,
        verbose_name=_('سایت')
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name=_('عنوان')
    )
    image = models.ImageField(
        upload_to='home_slider/',
        verbose_name=_('تصویر'),
    )

    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('لینک'),
    )

    class Meta:
        verbose_name = _('اسلایدر صفحه اصلی')
        verbose_name_plural = _('اسلایدر صفحه اصلی')

    def __str__(self):
        return self.title