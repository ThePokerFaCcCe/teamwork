from django import forms

from ..models import Note


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'text',
        ]

    def save(self, commit: bool = False):
        return super().save(commit)
