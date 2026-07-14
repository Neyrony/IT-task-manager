from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from it_task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager:task_type_detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager:position_detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        position = self.position.name if self.position else "No position"
        return f"{self.username} - {position}"

    def get_absolute_url(self):
        return reverse("manager:worker_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    class Priority(models.IntegerChoices):
        URGENT = 4, "Urgent"
        HIGH = 3, "High"
        MEDIUM = 2, "Medium"
        LOW = 1, "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks"
    )

    class Meta:
        ordering = ["-priority", "deadline"]

    def __str__(self):
        return f"{self.name} - {self.get_priority_display()} (is completed: {self.is_completed})"

    def get_absolute_url(self):
        return reverse("manager:task_detail", kwargs={"pk": self.pk})
