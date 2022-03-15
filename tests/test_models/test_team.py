from django.test.testcases import TestCase

from team.models import Member
from .creators import create_user, create_team


class TeamModelTest(TestCase):
    def test_owner_member_creates(self):
        user = create_user()
        team = create_team(creator=user)

        self.assertIsNotNone(
            Member.objects.filter(
                user=user, team=team,
                rank=Member.RankChoices.OWNER
            ).first(),
            msg="creator's member not created on team create"
        )
