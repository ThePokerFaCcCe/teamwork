from django.test.testcases import TestCase
from random import choice
from team.models import Member
from team.querysets import get_user_teams, get_team_with_members
from .creators import (create_user, create_team, create_member,
                       create_task, TaskStatusChoices)


class TeamModelTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def test_owner_member_creates(self):
        team = create_team(creator=self.user)

        self.assertIsNotNone(
            Member.objects.filter(
                user=self.user, team=team,
                rank=Member.RankChoices.OWNER
            ).first(),
            msg="creator's member not created on team create"
        )

    def test_get_user_teams(self):
        team1 = create_team(self.user)
        create_member(team1)
        create_team()
        team2 = create_team()
        create_member(team2, self.user)

        with self.assertNumQueries(1):
            teams = get_user_teams(self.user.pk)
            list(teams)

        self.assertEqual(
            teams.count(), 2,
            msg="returned teams are incorrect"
        )

    def __create_member_and_task(self, team, tasks_count=10) -> Member:
        member = create_member(team)
        for i in range(tasks_count):
            create_task(member, team, choice([TaskStatusChoices.DONE, TaskStatusChoices.SENT]))
        return member

    def test_get_team_with_members(self):
        team = create_team(self.user)
        members = [self.__create_member_and_task(team) for i in range(5)]

        with self.assertNumQueries(4):
            team = get_team_with_members(team.pk)
            for member in team.members.all():
                member.user.username
