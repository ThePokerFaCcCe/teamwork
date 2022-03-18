from .models import Task


def get_member_task(task_id) -> Task:
    """Return member's task and it's notes"""
    return Task.objects.filter(pk=task_id)\
        .select_related("member__user")\
        .prefetch_related("notes__member__user").first()
