# Django Built-in modules
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Local apps
from .forms import UserCreationForm, UserChangeForm, ProfileAdminForm, ProfileAdminFormset
from .models import User, MobilePhoneVerify, Profile
from utils.admin import DateTimeAdminMixin


class ProfileInline(admin.StackedInline):
    model = Profile
    form = ProfileAdminForm
    formset = ProfileAdminFormset
    fieldsets = (
        (
            None,
            {'fields': (
                'slug', 'display_name', 'position', 'bio',)}
        ),
    )
    classes = ('collapse',)
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (
            _('اطلاعات'),
            {'fields': ('username', 'first_name', 'last_name', 'mobile_number', 'email', 'avatar', 'password',)}
        ),
        (
            _('لاگ'),
            {'fields': ('last_login',)}
        ),
        (
            _('مجوز ها'),
            {
                # 'classes': ('collapse',),
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
            }
        ),
        *DateTimeAdminMixin.fieldsets,
    )
    add_fieldsets = (
        (
            _('اطلاعات'),
            {
                'fields': (
                    'username', 'password1', 'password2', 'first_name', 'last_name', 'mobile_number', 'email', 'avatar',
                )
            }
        ),
        (
            _('مجوز ها'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
                # 'classes': ('collapse',),
            }
        ),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('username', 'display_fullname', 'email', 'mobile_number', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'mobile_number', 'email',)
    ordering = ('-created',)
    inlines = (ProfileInline,)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'user_permissions':
            kwargs['queryset'] = Permission.objects.select_related('content_type')
        return super(UserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    @admin.display(description=_('نام و نام خانوادگی'), empty_value='-')
    def display_fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'


@admin.register(MobilePhoneVerify)
class MobilePhoneVerifyAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', *DateTimeAdminMixin.list_display)
