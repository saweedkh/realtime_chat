from modeltranslation.translator import translator, TranslationOptions
from .models import SiteGlobalSetting, SocialMediaSetting


class SiteGlobalSettingTranslationOptions(TranslationOptions):
    fields = ('name', 'slogan', 'copyright', 'main_banner', 'main_banner_link', 'about')


class SocialMediaSettingTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(SiteGlobalSetting, SiteGlobalSettingTranslationOptions)
translator.register(SocialMediaSetting, SocialMediaSettingTranslationOptions)
