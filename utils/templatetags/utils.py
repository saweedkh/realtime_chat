# Django Built-in modules
from django import template

# Local Apps
from utils.jdatetime import (
    humanize_datetime,
    pretty_jalali_datetime_format,
    show_current_time,
    standard_jalali_date_format,
)

register = template.Library()


@register.filter(name='humanize_datetime')
def humanize_jdatetime_template_tag(instance):
    return humanize_datetime(instance)


@register.filter(name='pretty_jalali')
def pretty_jalali_datetime_template_tag(instance):
    return pretty_jalali_datetime_format(instance)


@register.filter(name='standard_jalali_date')
def standard_jalali_date_template_tag(instance):
    return standard_jalali_date_format(instance)


@register.filter(name='jalali_current_time')
def jalali_current_time(text):
    return f'{text} {show_current_time()}'.strip()


@register.filter
def div(num, value):
    new_num =  num / value
    return int(new_num) if int(new_num) == new_num else new_num


@register.filter
def persian_numbers(value):
    persian_digits = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    result = ''.join(persian_digits.get(char, char) for char in str(value))
    return result


