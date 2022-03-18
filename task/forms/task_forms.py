from django import forms
from django.utils import timezone

from ..models import Task


class TaskCreateForm(forms.ModelForm):
    deadline = forms.IntegerField(max_value=366, min_value=1)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "member",
            "team",
            "deadline",
        ]

    def clean_deadline(self):
        deadline_days = self.cleaned_data['deadline']
        return timezone.timedelta(days=deadline_days) + timezone.now()

    def full_clean(self):
        super().full_clean()
        if self._errors:
            return

        if self.cleaned_data['member'].team_id != self.cleaned_data['team'].pk:
            self.add_error("member", 'Member not found')


class TaskUpdateStatusForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "status"
        ]
