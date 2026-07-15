from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from manager.models import Task, Position, TaskType


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        print(deadline)
        print(type(deadline))

        if deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past")

        return deadline

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees",
        )

        widgets = {
            "description": forms.Textarea(attrs={"rows": 1}),
            "deadline": forms.DateInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "class": "form-control"},
            ),
        }


class TaskCreateForm(TaskForm):
    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]

        if deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past")

        return deadline


class TaskUpdateForm(TaskForm):
    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]

        if timezone.now() > deadline != self.initial.get("deadline"):
            raise ValidationError("Deadline cannot be in the past")

        return deadline


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "position")


class TaskSearchForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name",)
        labels = {
            "name": "",
        }
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Search by name"})}


class WorkerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by any name"}),
    )


class TaskTypeSearchForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name",)
        labels = {
            "name": "",
        }
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Search by name"})}


class PositionSearchForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ("name",)
        labels = {
            "name": "",
        }
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Search by name"})}
