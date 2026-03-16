from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


# ---------------------------------------------------------------------------
# Constants — validated against in Task.__post_init__ and update_priority
# ---------------------------------------------------------------------------

PRIORITY_ORDER: dict[str, int] = {"high": 0, "medium": 1, "low": 2}

VALID_PRIORITIES: frozenset[str] = frozenset(PRIORITY_ORDER.keys())
VALID_TYPES: frozenset[str] = frozenset({"feeding", "walk", "medication", "appointment"})


# ---------------------------------------------------------------------------
# Task  (dataclass — Scheduler is the authoritative store)
# ---------------------------------------------------------------------------

@dataclass
class Task:
    description: str
    scheduled_at: datetime
    type: str                        # must be one of VALID_TYPES
    priority: str = "medium"         # must be one of VALID_PRIORITIES
    status: str = "pending"          # "pending" | "completed"
    pet_name: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        """Validate priority and type on construction so bad data never enters the system."""
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}, got '{self.priority}'")
        if self.type not in VALID_TYPES:
            raise ValueError(f"type must be one of {VALID_TYPES}, got '{self.type}'")

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
        """Update priority. Raises ValueError for unrecognised values."""
        pass


# ---------------------------------------------------------------------------
# Pet  (dataclass — NO tasks list; delegates all task operations to Scheduler)
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_needs: List[str] = field(default_factory=list)  # e.g. ["feeding x2", "daily walk"]

    # Internal reference to the owner's Scheduler.
    # Not part of __init__ — Owner sets this after creating the Pet.
    # repr=False / compare=False keeps it invisible to normal dataclass behaviour.
    _scheduler: Optional[Scheduler] = field(
        default=None, init=False, repr=False, compare=False
    )

    def add_task(self, task: Task) -> None:
        """Forward task to the Scheduler (single source of truth)."""
        pass

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID via the Scheduler. Returns True if removed."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet from the Scheduler."""
        pass

    def get_tasks_for_date(self, target_date: date) -> List[Task]:
        """Return this pet's tasks scheduled on target_date."""
        pass


# ---------------------------------------------------------------------------
# Owner  (plain class — owns the Scheduler; cascades removals)
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []
        self.scheduler: Scheduler = Scheduler()   # single Scheduler per owner

    def add_pet(self, name: str, species: str, age: int, care_needs: List[str]) -> Pet:
        """Create a Pet, wire its _scheduler reference, register it, and return it."""
        pass

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet AND cascade-delete all its tasks from the Scheduler.
        Returns True if the pet was found and removed, False otherwise."""
        pass

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return the Pet with the given name, or None if not found."""
        pass

    def list_pets(self) -> List[Pet]:
        """Return all registered pets."""
        pass


# ---------------------------------------------------------------------------
# Scheduler  (single source of truth for all Task objects)
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Register a task."""
        pass

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID. Returns True if found and removed."""
        pass

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to the named pet.
        Added to fix the missing Pet ↔ Scheduler navigation path."""
        pass

    def get_tasks_for_date(self, target_date: date) -> List[Task]:
        """Return all tasks scheduled on target_date."""
        pass

    def get_today_tasks(self) -> List[Task]:
        """Return all tasks scheduled for today (delegates to get_tasks_for_date)."""
        pass

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return a new list sorted by scheduled_at (earliest first)."""
        pass

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return a new list sorted high → medium → low using PRIORITY_ORDER."""
        pass

    def get_next_tasks(self, limit: int = 5) -> List[Task]:
        """Return the next `limit` PENDING tasks ordered by scheduled_at.
        Filters status='pending' first to avoid returning completed tasks."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks with status='pending'."""
        pass
