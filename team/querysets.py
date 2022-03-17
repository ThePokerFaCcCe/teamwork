from django.db.models import QuerySet
from .models import Team, Member


def get_user_teams(user_id) -> QuerySet:
    """Return teams that user joined/created"""
    return Team.objects.filter(
        id__in=Member.objects.only('team_id')
        .filter(user_id=user_id).
        values_list('team_id', flat=True)
    ).select_related("creator")


def get_team_with_members(team_id) -> QuerySet:
    """Return team and it's members with tasks prefetched"""
    return Team.objects.filter(id=team_id)\
        .prefetch_related("members__tasks", "members__user")\
        .first()
