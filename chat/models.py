from datetime import datetime
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from multiselectfield import MultiSelectField






# Local Import
from utils.datetime import check_and_make_aware
from utils.models import AbstractDateTimeModel

# Third party Import 
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from smart_selects.db_fields import ChainedForeignKey


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



# class Permission(AbstractDateTimeModel):
#     name = models.CharField(
#         _(""), max_length=50)




class Link(AbstractDateTimeModel):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("کاربر"),
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group, 
        verbose_name=_("گروه"), 
        on_delete=models.CASCADE,
        related_name='groupmember',
    )
    link = models.CharField(
        _("لینک"), 
        max_length=255,
    )
    expired = models.DateTimeField(
        _("تاریخ انقضا"), 
        blank=True,
        null=True,
    )
    member_limit = models.PositiveIntegerField(
        _("محدودیت اعضا"),
        default=0,
        help_text=_('مقدار 0 به منظور بدون محدودیت است'),
    )
    joined_member = models.PositiveIntegerField(
        _("تعداد کاربران عضو شده"),
        default=0,
    )
    
    @property
    def is_active(self):
        if self.expired and (check_and_make_aware(datetime.now()) - self.expired).seconds > 0:
            return {'message': _('لینک منقضی شده است.'), 'status': 404}
        elif  self.member_limit >= self.joined_member:
            return {'message': _('تعداد کاربران عضو شده بیشتر از حد مجاز است.'), 'status': 404}
        
        return {'status': 200,}
    
    
    @property
    def increase_joined_member(self,):
        self.joined_member += 1
        self.save()
        return {'status': 200,}
        
        
    
    def __str__(self) -> str:
        return f'لینک {self.user.fullname} - گروه {self.group.name}'
    
    class Meta:
        verbose_name = _('لینک')
        verbose_name_plural = _('لینک ها')
        


    
class GroupMember(AbstractDateTimeModel):
    
    ADD_USER = 'add-user'
    CHANGE_GROUP_INFO = 'change-group-info'
    DELETE_MESSAGES = 'delete-messages'
    BAN_USERS = 'ban-users'
    INVITE_USERS = 'invite-users'
    PIN_MESSAGES = 'pin-messages'
    REMAIN_ANONYMOUS = 'remain-anonymous'
    ADD_ADMIN = 'add-admin'
    
    
    PERMISSION_CHOICES = (
        (ADD_USER,'Add User',),
        (CHANGE_GROUP_INFO, 'Change Group Info', ),
        (DELETE_MESSAGES, 'Delete Messages', ),
        (BAN_USERS, 'Ban Users', ),
        (INVITE_USERS, 'Inviite Users Via Link', ),
        (PIN_MESSAGES, 'Pin Messsges', ),
        (REMAIN_ANONYMOUS, 'Remain Anonymous', ),
        (ADD_ADMIN, 'Add New Admin', ),
    )
    
    
    
    SEND_MESSAGES = 'send-messages'
    ADD_MEMBER = 'add-member'
    USER_PIN_MESSAGES = 'user-pin-messages'
    USER_CHANGE_GROUP_INFO = 'user-change-group-info'

    
    
    LIMITED_CHOICES = (
        (SEND_MESSAGES, 'Send Messages'),
        (ADD_MEMBER, 'Add Member'),
        (USER_PIN_MESSAGES, 'Pin Messages'),
        (CHANGE_GROUP_INFO, 'Change Group Info'),
    )
    
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("کاربر"), 
        on_delete=models.CASCADE,
        # related_name='groupmember'
    )
    group = models.ForeignKey(
        Group, 
        verbose_name=_("گروه"), 
        on_delete=models.CASCADE,
        related_name='members',
    )
    admin_permissions = MultiSelectField(
        verbose_name=_("مجوزها"), 
        blank=True,
        null=True,
        choices=PERMISSION_CHOICES
    )
    user_limited = MultiSelectField(
        verbose_name=_("محدودیت ها"), 
        blank=True,
        null=True,
        choices=LIMITED_CHOICES
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
        unique_together = ('user', 'group')

    
    
    
  
  
  
    