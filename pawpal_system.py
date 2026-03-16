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
        self.status = "completed"

    def is_due_today(self, target_date: date) -> bool:
        """Return True if the task is scheduled on target_date."""
        return self.scheduled_at.date() == target_date

    def is_overdue(self, current_datetime: datetime) -> bool:
        """Return True if the task is still pending and scheduled_at is in the past."""
        return self.status == "pending" and self.scheduled_at < current_datetime

    def update_priority(self, new_priority: str) -> None:
        """Update priority. Raises ValueError for unrecognised values."""
        if new_priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}, got '{new_priority}'")
        self.priority = new_priority


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
        """Stamp the pet name onto the task and forward it to the Scheduler."""
        task.pet_name = self.name
        self._scheduler.add_task(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID via the Scheduler. Returns True if removed."""
        return self._scheduler.remove_task(task_id)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet from the Scheduler."""
        return self._scheduler.get_tasks_for_pet(self.name)

    def get_tasks_for_date(self, target_date: date) -> List[Task]:
        """Return this pet's tasks scheduled on target_date."""
        return [t for t in self.get_tasks() if t.is_due_today(target_date)]


# ---------------------------------------------------------------------------
# Owner  (plain class — owns the Scheduler; cascades removals)
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []
        self.scheduler: Scheduler = Scheduler()  # single Scheduler per owner

    def add_pet(self, name: str, species: str, age: int, care_needs: List[str]) -> Pet:
        """Create a Pet, wire its _scheduler reference, register it, and return it."""
        pet = Pet(name, species, age, care_needs)
        pet._scheduler = self.scheduler
        self.pets.append(pet)
        return pet

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet and cascade-delete its tasks; returns True if found."""
        pet = self.get_pet(pet_name)
        if pet is None:
            return False
        # Cascade: remove every task that belongs to this pet
        for task in pet.get_tasks():
            self.scheduler.remove_task(task.id)
        self.pets.remove(pet)
        return True

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return the Pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def list_pets(self) -> List[Pet]:
        """Return all registered pets."""
        return self.pets


# ---------------------------------------------------------------------------
# Scheduler  (single source of truth for all Task objects)
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Register a task."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID. Returns True if found and removed."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to the named pet."""
        return [t for t in self.tasks if t.pet_name == pet_name]

    def get_tasks_for_date(self, target_date: date) -> List[Task]:
        """Return all tasks scheduled on target_date."""
        return [t for t in self.tasks if t.is_due_today(target_date)]

    def get_today_tasks(self) -> List[Task]:
        """Return all tasks scheduled for today."""
        return self.get_tasks_for_date(date.today())

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return a new list sorted by scheduled_at (earliest first)."""
        return sorted(tasks, key=lambda t: t.scheduled_at)

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return a new list sorted high → medium → low using PRIORITY_ORDER."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority])

    def get_next_tasks(self, limit: int = 5) -> List[Task]:
        """Return the next `limit` pending tasks ordered by scheduled_at."""
        pending = self.get_pending_tasks()
        return self.sort_tasks_by_time(pending)[:limit]

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks with status='pending'."""
        return [t for t in self.tasks if t.status == "pending"]
