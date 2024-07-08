from modeltranslation.translator import translator, TranslationOptions
from .models import User, MobilePhoneVerify, Profile 


class UserTranslationOptions(TranslationOptions):
    fields = ('first_name','last_name', )


class ProfileTranslationOptions(TranslationOptions):
    fields = ('bio', 'display_name', 'position',)


translator.register(User, UserTranslationOptions, )
translator.register(Profile, ProfileTranslationOptions, )
