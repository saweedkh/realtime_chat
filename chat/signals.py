from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# local import
from .models import Group, GroupMember


@receiver(post_save, sender=Group)
def create_group_member(sender, instance, created, **kwargs):
    if created:
        GroupMember.objects.create(
            user=instance.creator,
            group=instance,
        )
        
@receiver(pre_delete, sender=Group)
def delete_group_members(sender, instance, **kwargs):
    GroupMember.objects.filter(group=instance).delete()