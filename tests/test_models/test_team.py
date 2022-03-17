from django.test.testcases import TestCase

from team.models import Member
from team.querysets import get_user_teams
from .creators import create_user, create_team, create_member


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

    def test_get_user_teams(self):
        user = create_user()

        team1 = create_team(user)
        create_member(team1)
        create_team()
        team2 = create_team()
        create_member(team2, user)

        with self.assertNumQueries(1):
            teams = get_user_teams(user.pk)
            list(teams)

        self.assertEqual(
            teams.count(), 2,
            msg="returned teams are incorrect"
        )
