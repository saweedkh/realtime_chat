# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.models import LogEntry

# Local Apps
from .models import (
    SiteGlobalSetting,
    SocialMediaSetting,
    PhoneNumber,
    Address,
    HomePageSlider,
)
from account.models import User
from utils.admin import DateTimeAdminMixin


class PhoneAdmin(admin.TabularInline):
    model = PhoneNumber
    extra = 0

class AddressAdmin(admin.TabularInline):
    model = Address
    extra = 0


class HomePageSliderAdmin(admin.TabularInline):
    model = HomePageSlider
    extra = 0


@admin.register(SiteGlobalSetting)
class SiteGlobalSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('عمومی'), {'fields': (
            'name', 'slogan', 'copyright', 'video',
        )}),
        (_('لوگو و فاوآیکون'), {'fields': (
            'logo', 'favicon',
        )}),
        (_('بنر اصلی سایت'), {'fields': (
            'main_banner', 'main_banner_link',
        )}),
        (_('راه های ارتباطی'), {'fields': (
            'email', 'fax',
        )}),
        (_('فوتر'), {'fields': (
            'about',
        )}),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    inlines = (PhoneAdmin,AddressAdmin, HomePageSliderAdmin)
    list_display = ('display_page_title',)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_('تنظیمات'), empty_value='-')
    def display_page_title(self, obj):
        return obj.__str__()


@admin.register(SocialMediaSetting)
class SocialMediaSettingAdmin(admin.ModelAdmin):
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name',)
    search_fields = ('name',)


# Add Django Log Entry to admin

class UserListFilter(admin.SimpleListFilter):
    title = _('کاربر')
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        users = ()
        for user in User.objects.filter(is_superuser=True, is_staff=True):
            users += ((user.id, f'{user.username} | {user.fullname}',),)
        return users

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user=self.value())


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_filter = (UserListFilter, 'content_type', 'action_flag',)
    list_select_related = ('user', 'content_type',)
    search_fields = ('object_repr', 'change_message')
    list_display = ('action_time', 'display_name', 'content_type', 'action_flag',)
    date_hierarchy = 'action_time'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description=_('کاربر'), empty_value='-')
    def display_name(self, obj):
        return f"{obj.user.username} | {obj.user.fullname}"
