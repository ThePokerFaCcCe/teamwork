from django.db.models import QuerySet
from .models import Team, Member


def get_user_teams(user_id) -> QuerySet:
    """Return teams that user joined/created"""
    return Team.objects.filter(
        id__in=Member.objects.only('team_id')
        .filter(user_id=user_id).
        values_list('team_id', flat=True)
    ).select_related("creator")
