from datetime import datetime, timedelta
from typing import List
from .models import Task, Priority

BLOCK_SIZES = [15, 30, 60]

def schedule_tasks(tasks: List[Task], block_size: int = 60):
    block_size = block_size if block_size in BLOCK_SIZES else 60
    start_hour = 8
    end_hour = 18
    current = datetime.utcnow().replace(hour=start_hour, minute=0, second=0, microsecond=0)
    tasks_sorted = sorted(tasks, key=lambda t: t.priority.value)  # high first
    for task in tasks_sorted:
        duration = timedelta(minutes=task.duration_minutes)
        if duration.seconds % (block_size * 60):
            duration = timedelta(minutes=((duration.seconds // (block_size * 60) + 1) * block_size))
        task.scheduled_start = current
        task.scheduled_end = current + duration
        current = task.scheduled_end
        if current.hour >= end_hour:
            current = current.replace(hour=start_hour) + timedelta(days=1)
