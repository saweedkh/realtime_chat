from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from chat.models import Group, GroupMember

# Register your models here.


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'creator',
        'group_id',
        'member_count',
        'display_gallery_image_thumbnail',
    )
    
    @admin.display(description=_('تعداد اعضا'), empty_value='-')
    def member_count(self, obj):
        members = obj.members.count()
        return members
    
    @admin.display(description=_('نمایش تصویر'), empty_value='-')
    def display_gallery_image_thumbnail(self, obj):
        image_url = obj.get_image
        print(image_url)
        return mark_safe(f'''<a target="_blank" href="{image_url}">
        <img src="{image_url}" width="60" height="60" class="circle-image" load="lazy" /></a>''')

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    
@admin.register(GroupMember)    
class GroupMemberAdmin(admin.ModelAdmin):
    pass