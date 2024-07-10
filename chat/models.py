from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Local Import
from utils.models import AbstractDateTimeModel

# Third party Import 
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Group(AbstractDateTimeModel):
    
    PRIVATE = 1
    PUBLIC = 2
    
    GROUP_TYPE_CHOICES = (
        (PRIVATE, _('خصوصی'), ),
        (PUBLIC, _('عمومی'), ),
    )
    
    uuid = models.UUIDField(
        _("آیدی یکتا"),
        default=uuid4,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(
        _("نام"), 
        max_length=255,
    )
    member_limit = models.PositiveIntegerField(
        _("محدودیت اعضا"),
        default=0,
    )
    description = models.TextField(
        _("توضیحات"), 
        blank=True,
        null=True,
    )
    group_id = models.CharField(
        _("آیدی گروه"), 
        max_length=25,
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("سازنده"), 
        on_delete=models.CASCADE,
        related_name='group_creator',
    )
    type = models.PositiveSmallIntegerField(
        _("نوع گروه"),
        choices=GROUP_TYPE_CHOICES,
        default=PRIVATE,
    )
    image = models.ImageField(
        _("تصویر"), 
        upload_to='group/image/', 
        blank=True, 
        null=True,
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(250, 250)],
        format='PNG',
        options={'quality': 70}
    )
    
    ban_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("لیست مسدودها"),
        blank=True,
        related_name='group_ban_list',
    )
    
    
    def __str__(self):
        return self.name
    
    
    class Meta : 
        verbose_name = _('گروه')
        verbose_name_plural = _('گروه ها')
        
    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image_thumbnail.url
        except:
            image = settings.DEFAULT_GROUP_IMAGE_PATH
            
        print(image)
        return image
    
    
    
class Role(AbstractDateTimeModel):
    pass  

class Link(AbstractDateTimeModel):
    pass  


    
class GroupMember(AbstractDateTimeModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("کاربر"), 
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group, 
        verbose_name=_("گروه"), 
        on_delete=models.CASCADE,
        related_name='members',
    )
    user_role = models.ForeignKey(
        Role, 
        verbose_name=_("سطح دسترسی"), 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    link = models.ManyToManyField(
        Link, 
        verbose_name=_("لینک ها"),
        blank=True,
    )
    
    def __str__(self):
        return f'{self.user.fullname}-{self.group.name}'
    
    class Meta:
        verbose_name = _('عضو گروه')
        verbose_name_plural = _('اعضای گروه ها')
        
    
    
    
  
  
  
    