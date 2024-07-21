from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


# local import 
from chat.forms import GroupMemberForm, LinkAdminForm
from chat.models import Group, GroupMember, Link
from utils.admin import DateTimeAdminMixin




class GroupMemberInlineAdmin(admin.TabularInline):
    form = GroupMemberForm
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
    search_fields = ('name',)
    
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
                'admin_permissions',
                'link',
            ),
        }),
    )
    
    list_filter = ('user', 'group')
    list_display = ('user', 'group', 'admin_permissions')
 
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    
    fieldsets = (
        ("مشخصات لینک", {
            "fields": (
                'user',
                'group',
                'link',
            ),
        }),
        
        ("محدودیت ها", {
            "fields": (
                'member_limit',
                'joined_member',
                'expired',
            ),
        }),
        *DateTimeAdminMixin.fieldsets,
    )
    
    list_display = ('link', 'user', 'group',)
    search_fields = ('user__fullname', 'group__name', 'link')
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    autocomplete_fields = ('user', 'group',)
    list_filter = ('group', 'user',)

    
    class Media:
        js = ('js/admin_link_form.js',)

