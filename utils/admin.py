# django import
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# local import
from seo.admin import SeoAdminMixin


class DateTimeAdminMixin(admin.ModelAdmin):
    fields = ('created', 'updated',)
    fieldsets = (
        (_('تاریخچه'), { 'fields': ('jcreated', 'jupdated',)}),
    )
    readonly_fields = ('jcreated', 'jupdated',)
    list_display = ('jcreated', 'jupdated',)
    list_filter = ('created', 'updated',)
    date_hierarchy = 'created'


class StaticPageAdminMixin(admin.ModelAdmin):
    fieldsets = (
        (_('محتوا'), {'fields': (
            'content',
        )}),
        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'slug',)
    list_display = ('display_page_title', 'display_page_in_site', *SeoAdminMixin.list_display,)
    inlines = (*SeoAdminMixin.inlines,)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_('صفحه'), empty_value='-')
    def display_page_title(self, obj):
        return obj.__str__()

    @admin.display(description=_('نمایش در وب گاه'), empty_value='-')
    def display_page_in_site(self, obj):
        return mark_safe(f'<a target="_blank" href="{self.view_on_site(obj)}">{_("نمایش")}</a>')


class PageOptionAdminMixin(admin.ModelAdmin):
    fieldsets = (
        (_('تنظیمات صفحه'), { 'fields': ('parallax_image',)}),
    )
