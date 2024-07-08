# django import
from django.utils.translation import get_language

# third import
from jdatetime import datetime as jalali_datetime
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def convert_to_jalali(instance):
    lang_code = get_language()
    if lang_code == 'en':
        return instance.strftime('%d/%M/%Y')
    return jalali_datetime.fromgregorian(datetime=instance)


def standard_jalali_datetime_format(instance):
    lang_code = get_language()
    if lang_code == 'en':
        return instance.strftime('%d/%M/%Y')
    return convert_to_jalali(instance).strftime('%H:%M %Y/%m/%d')


def pretty_jalali_datetime_format(instance):
    lang_code = get_language()
    if lang_code == 'en':
        return instance.strftime('%d/%M/%Y')
    _instance = convert_to_jalali(instance)
    months = ('فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')
    return _instance.strftime('%d {} %Y'.format(months[int(_instance.strftime('%m')) - 1]))


def standard_jalali_date_format(instance):
    lang_code = get_language()
    if lang_code == 'en':
        return instance.strftime('%d/%M/%Y')
    _instance = convert_to_jalali(instance)
    return _instance.strftime('%Y/%m/%d')


def show_current_time():
    _instance = convert_to_jalali(datetime.now())
    days = ('شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه')
    months = ('فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')
    return _instance.strftime(
        '{} %d {} %Y'.format(
            days[_instance.weekday()],
            months[int(_instance.strftime('%m')) - 1]
        )
    )


def humanize_datetime(instance):
    """
    Translates datetime values into verbal phrases
    :param instance: gregorian/jalali datetime instance
    :return: e.g => a few moments ago
    """
    lang_code = get_language()
    if lang_code == 'en':
        return instance.strftime('%d/%M/%Y')
    if isinstance(instance, datetime):
        difference = datetime.now() - instance.replace(tzinfo=None)
    else:
        raise ValueError('Enter standard datetime instance(gregorian/jalali).')

    days_past = difference.days
    seconds_past = difference.seconds

    if days_past == 0:
        if seconds_past < 10:
            return _('چند لحظه قبل')
        if seconds_past < 60:
            return '{0} {1}'.format(int(seconds_past), _('ثانیه قبل'))
        if seconds_past < 120:
            return _('یک دقیقه قبل')
        if seconds_past < 3600:
            return '{0} {1}'.format(int(seconds_past / 60), _('دقیقه قبل'))
        if seconds_past < 7200:
            return _('یک ساعت قبل')
        if seconds_past < 86400:
            return '{0} {1}'.format(int(seconds_past / 3600), _('ساعت قبل'))
    if days_past == 1:
        return _('دیروز')
    if days_past < 7:
        return '{0} {1}'.format(int(days_past), _('روز قبل'))
    if days_past < 31:
        return '{0} {1}'.format(int(days_past / 7), _('هفته قبل'))
    if days_past < 365:
        return '{0} {1}'.format(int(days_past / 30), _('ماه قبل'))
    return '{0} {1}'.format(int(days_past / 365), _('سال قبل'))
