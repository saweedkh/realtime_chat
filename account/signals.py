# Django Built-in modules
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Local apps
from .models import Profile


@receiver(pre_save, sender=Profile)
def set_slug_for_user_profile(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user.username)
