from django import forms
from django.contrib.auth import get_user_model
from .models import Team, Member

User = get_user_model()


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'description',
            'creator',
        ]


class MemberCreateForm(forms.ModelForm):
    username = forms.CharField()
    user = None

    class Meta:
        model = Member
        fields = [
            'team',
            'username',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError("User with entered username not found")
        self.user = user
        return username

    def full_clean(self):
        super().full_clean()
        if not self._errors:
            member = Member.objects.only('id').filter(
                user=self.user,
                team=self.cleaned_data.get('team')
            )
            if member.exists():
                self.add_error('username', "This user is already in team")

    def save(self, commit: bool = True):
        self.instance.user = self.user
        return super().save(commit=commit)
