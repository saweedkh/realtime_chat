# Django Built-in modules
from django.utils.translation import gettext_lazy as _

# Local Apps
from order.models import Order

# Third Party Packages
from django_filters import FilterSet, filters


class OrderFilter(FilterSet):
    tracking_code = filters.CharFilter(lookup_expr='contains', label=_('شماره پیگیری'))

    class Meta:
        model = Order
        fields = ('tracking_code', 'order_status',)
