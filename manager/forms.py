from django import forms
from django.contrib.auth import get_user_model

from manager.models import Task


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees"
        )

        widgets = {
            "description": forms.Textarea(attrs={"rows": 1}),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
