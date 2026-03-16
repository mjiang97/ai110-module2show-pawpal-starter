from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


# Priority levels from highest to lowest — used for sorting
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    description: str
    scheduled_at: datetime
    type: str                          # e.g. "feeding", "walk", "medication", "appointment"
    priority: str = "medium"           # "high" | "medium" | "low"
    status: str = "pending"            # "pending" | "completed"
    pet_name: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        pass

    def is_due_today(self, target_date: date) -> bool:
        """Return True if the task is scheduled on target_date."""
        pass

    def is_overdue(self, current_datetime: datetime) -> bool:
        """Return True if the task is still pending and scheduled_at is in the past."""
        pass

    def update_priority(self, new_priority: str) -> None:
        """Update the task's priority. Accepts 'high', 'medium', or 'low'."""
        pass


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_needs: List[str] = field(default_factory=list)   # e.g. ["feeding x2", "daily walk"]
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a Task to this pet."""
        pass

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID. Returns True if found and removed, False otherwise."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        pass

    def get_tasks_for_date(self, target_date: date) -> List[Task]:
        """Return tasks scheduled on target_date."""
        pass


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, name: str, species: str, age: int, care_needs: List[str]) -> Pet:
        """Create a new Pet, register it, and return it."""
        pass

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name. Returns True if found and removed, False otherwise."""
        pass

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return the Pet with the given name, or None if not found."""
        pass

    def list_pets(self) -> List[Pet]:
        """Return all registered pets."""
        pass


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Register a task with the scheduler."""
        pass

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID. Returns True if found and removed, False otherwise."""
        pass

    def get_tasks_for_date(self, target_date: date) -> List[Task]:
        """Return all tasks scheduled on target_date."""
        pass

    def get_today_tasks(self) -> List[Task]:
        """Return all tasks scheduled for today."""
        pass

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by scheduled_at (earliest first)."""
        pass

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority (high → medium → low)."""
        pass

    def get_next_tasks(self, limit: int = 5) -> List[Task]:
        """Return the next `limit` pending tasks ordered by scheduled_at."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks with status 'pending'."""
        pass
