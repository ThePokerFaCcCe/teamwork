from django.dispatch import receiver
from django.db.models.signals import post_save

from core.utils import delete_instance_on_error
from .models import Team, Member


@receiver(post_save, sender=Team, dispatch_uid="create_team_owner_member")
def create_team_owner_member(sender, instance: Team, created, **_):
    if not created:
        return
    member = Member()
    member.user = instance.creator
    member.team = instance
    member.rank = Member.RankChoices.OWNER
    delete_instance_on_error(member.save, instance=instance)
