from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from manager.models import TaskType, Position, Task, Worker


class BasedNameModelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 20


@admin.register(TaskType)
class TaskTypeAdmin(BasedNameModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(BasedNameModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    list_per_page = 20
    fieldsets = UserAdmin.fieldsets + (("Position", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name", "email"),
            },
        ),
        (
            "Position",
            {
                "fields": ("position",),
            },
        ),
    )

    def get_queryset(self, request):
        return get_user_model().objects.select_related("position")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    )
    list_per_page = 20
    search_fields = ("name",)
    list_filter = (
        "is_completed",
        "priority",
        "task_type",
    )

    def get_queryset(self, request):
        return Task.objects.select_related("task_type")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "assignees":
            kwargs["queryset"] = get_user_model().objects.select_related("position")

        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.unregister(Group)
