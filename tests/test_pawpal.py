import pytest
from datetime import datetime
from pawpal_system import Owner, Task


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def make_owner() -> Owner:
    """Return a fresh Owner with one pet wired to the Scheduler."""
    owner = Owner("Macy")
    owner.add_pet("Buddy", "dog", 3, ["feeding x2", "daily walk"])
    return owner


def make_task(**kwargs) -> Task:
    """Return a basic Task, letting callers override any field."""
    defaults = dict(
        description="Morning walk",
        scheduled_at=datetime(2026, 3, 15, 8, 0),
        type="walk",
        priority="medium",
    )
    defaults.update(kwargs)
    return Task(**defaults)


# ---------------------------------------------------------------------------
# Task Completion Tests
# ---------------------------------------------------------------------------

class TestMarkCompleted:
    def test_status_changes_to_completed(self):
        """mark_completed() must flip status from 'pending' to 'completed'."""
        task = make_task()
        assert task.status == "pending"
        task.mark_completed()
        assert task.status == "completed"

    def test_mark_completed_is_idempotent(self):
        """Calling mark_completed() twice should not raise and status stays 'completed'."""
        task = make_task()
        task.mark_completed()
        task.mark_completed()
        assert task.status == "completed"

    def test_completed_task_not_in_pending(self):
        """A completed task must not appear in the Scheduler's pending list."""
        owner = make_owner()
        buddy = owner.get_pet("Buddy")
        task = make_task()
        buddy.add_task(task)

        task.mark_completed()

        pending_ids = [t.id for t in owner.scheduler.get_pending_tasks()]
        assert task.id not in pending_ids


# ---------------------------------------------------------------------------
# Task Addition Tests
# ---------------------------------------------------------------------------

class TestTaskAddition:
    def test_adding_task_increases_count(self):
        """Adding one task to a pet should increase its task count by 1."""
        owner = make_owner()
        buddy = owner.get_pet("Buddy")
        before = len(buddy.get_tasks())

        buddy.add_task(make_task())

        assert len(buddy.get_tasks()) == before + 1

    def test_adding_multiple_tasks_increases_count(self):
        """Adding N tasks should increase the count by exactly N."""
        owner = make_owner()
        buddy = owner.get_pet("Buddy")
        before = len(buddy.get_tasks())

        for _ in range(3):
            buddy.add_task(make_task())

        assert len(buddy.get_tasks()) == before + 3

    def test_task_belongs_to_correct_pet(self):
        """A task added to Buddy must not appear in Luna's task list."""
        owner = make_owner()
        owner.add_pet("Luna", "cat", 5, [])
        buddy = owner.get_pet("Buddy")
        luna = owner.get_pet("Luna")

        buddy.add_task(make_task(description="Buddy's walk"))

        buddy_descriptions = [t.description for t in buddy.get_tasks()]
        luna_descriptions  = [t.description for t in luna.get_tasks()]
        assert "Buddy's walk" in buddy_descriptions
        assert "Buddy's walk" not in luna_descriptions

    def test_added_task_appears_in_scheduler(self):
        """A task added via pet.add_task() must also be visible in the Scheduler."""
        owner = make_owner()
        buddy = owner.get_pet("Buddy")
        task = make_task()

        buddy.add_task(task)

        scheduler_ids = [t.id for t in owner.scheduler.tasks]
        assert task.id in scheduler_ids
