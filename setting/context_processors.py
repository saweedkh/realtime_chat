from setting.models import (
    Address,
    SiteGlobalSetting,
    SocialMediaSetting,
    PhoneNumber
)


def global_settings(request):
    _global_settings = SiteGlobalSetting.objects.last()
    if not _global_settings:
        _global_settings = SiteGlobalSetting.objects.create(name='Saweedkh')
    socials = SocialMediaSetting.objects.all()
    site_phone = PhoneNumber.objects.all()
    addresses = Address.objects.all() 
    return {'global_settings': _global_settings, 'socials': socials, 'site_phone': site_phone, 'addresses': addresses}

