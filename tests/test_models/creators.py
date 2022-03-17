from uuid import uuid4
from django.contrib.auth import get_user_model

from team.models import Team, Member

User = get_user_model()


def create_user(**kwargs) -> User:
    kwargs.setdefault('username', f"u{uuid4().hex[:20]}")
    return User.objects.create_user(**kwargs)


def create_team(creator=None, **kwargs) -> Team:
    kwargs.setdefault("name", "OurTeam")
    return Team.objects.create(
        creator=creator or create_user(),
        **kwargs)


def create_member(team=None, user=None,
                  rank=Member.RankChoices.NORMAL,
                  **kwargs) -> Member:
    return Member.objects.create(
        team=team or create_team(),
        user=user or create_user(),
        rank=rank, **kwargs
    )
