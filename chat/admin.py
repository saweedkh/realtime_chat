from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


# local import 
from chat.forms import LinkAdminForm
from chat.models import Group, GroupMember, Link
from utils.admin import DateTimeAdminMixin




class GroupMemberInlineAdmin(admin.TabularInline):
    model = GroupMember
    extra = 0
    autocomplete_fields = ('link', 'user')
    classes = ('collapse',)
    verbose_name = _('اعضای گروه')
    verbose_name_plural = _('اعضای گروه')

    
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ('اطلاعات گروه', {
            "fields": (
                'uuid',
                "name",
                'creator',
                'type',
            ),
        }),
        ('مشخصات گروه', {
            "fields": (
                'group_id',
                'image',
                "description",
            ),
            "classes": ('collapse',),
        }),
        ('محدودیت گروه', {
            "fields": (
                'member_limit',
                'ban_list',
            ),
            "classes": ('collapse',),
        }),
        *DateTimeAdminMixin.fieldsets
    )
    
    list_display = (
        'name',
        'creator',
        'group_id',
        'member_count',
        'display_gallery_image_thumbnail',
    )
    
    readonly_fields = ('uuid', *DateTimeAdminMixin.readonly_fields, )
    inlines = (GroupMemberInlineAdmin,)
    autocomplete_fields = ('ban_list',)
    
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
    
    fieldsets = (
        ('اطلاعات کاربر این گروه', {
            "fields": (
                'user',
                'group',
                'user_role',
                'link',
            ),
        }),
    )
    
    list_filter = ('user', 'group')
    
    
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    
    search_fields = ('user__fullname', 'group__name', 'link')

    
    class Media:
        js = ('js/admin_link_form.js',)
