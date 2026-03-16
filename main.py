from datetime import datetime
from pawpal_system import Owner, Task

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

owner = Owner("Macy")

buddy = owner.add_pet("Buddy", "dog", 3, ["feeding x2", "daily walk"])
luna  = owner.add_pet("Luna",  "cat", 5, ["feeding x2", "medication"])

# ---------------------------------------------------------------------------
# Tasks — all scheduled for today so they show up in Today's Schedule
# ---------------------------------------------------------------------------

today = datetime.now().date()

buddy.add_task(Task(
    description="Morning walk around the block",
    scheduled_at=datetime(today.year, today.month, today.day, 7, 30),
    type="walk",
    priority="high",
))

buddy.add_task(Task(
    description="Breakfast — 1 cup dry kibble",
    scheduled_at=datetime(today.year, today.month, today.day, 8, 0),
    type="feeding",
    priority="high",
))

luna.add_task(Task(
    description="Breakfast — half can wet food",
    scheduled_at=datetime(today.year, today.month, today.day, 8, 15),
    type="feeding",
    priority="medium",
))

luna.add_task(Task(
    description="Thyroid medication — 1 pill in food",
    scheduled_at=datetime(today.year, today.month, today.day, 12, 0),
    type="medication",
    priority="high",
))

buddy.add_task(Task(
    description="Evening walk — 30 minutes",
    scheduled_at=datetime(today.year, today.month, today.day, 18, 0),
    type="walk",
    priority="medium",
))

# ---------------------------------------------------------------------------
# Print today's schedule
# ---------------------------------------------------------------------------

scheduler = owner.scheduler
today_tasks = scheduler.sort_tasks_by_time(scheduler.get_today_tasks())

print("=" * 50)
print(f"  PawPal+ — Today's Schedule ({today})")
print(f"  Owner: {owner.name}  |  Pets: {', '.join(p.name for p in owner.list_pets())}")
print("=" * 50)

if not today_tasks:
    print("  No tasks scheduled for today.")
else:
    for task in today_tasks:
        time_str    = task.scheduled_at.strftime("%I:%M %p")
        status_icon = "✓" if task.status == "completed" else "•"
        print(f"  {status_icon} [{time_str}] ({task.priority.upper():6}) [{task.pet_name}] {task.description}")

print("=" * 50)
print(f"  Pending: {len(scheduler.get_pending_tasks())}  |  Next up: {scheduler.get_next_tasks(1)[0].description}")
print("=" * 50)
