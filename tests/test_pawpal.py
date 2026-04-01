from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ---------- Helpers ----------

def make_scheduler(minutes=120):
    """Creates a basic Owner + Pet + Scheduler for reuse across tests."""
    owner = Owner("Jordan", available_minutes=minutes)
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


# ---------- Existing Tests ----------

def test_mark_complete_changes_status():
    """Task completion: mark_complete() should set completed to True."""
    task = Task("Morning walk", 20, "daily", "high")
    assert task.completed == False

    task.mark_complete()

    assert task.completed == True


def test_add_task_increases_pet_task_count():
    """Task addition: adding a task to a Pet should increase its task count."""
    pet = Pet("Mochi", "dog", 3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feed breakfast", 10, "daily", "high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Play fetch", 25, "daily", "medium"))
    assert len(pet.tasks) == 2


# ---------- Sorting Correctness ----------

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks ordered earliest to latest start_time."""
    owner, pet, scheduler = make_scheduler()

    # Add tasks out of chronological order
    pet.add_task(Task("Evening walk",  20, "daily", "medium", start_time="18:30"))
    pet.add_task(Task("Feed breakfast", 10, "daily", "high",  start_time="07:30"))
    pet.add_task(Task("Play fetch",    25, "daily", "medium", start_time="15:00"))

    scheduler.generate_plan()
    sorted_tasks = scheduler.sort_by_time()

    times = [t.start_time for t in sorted_tasks]
    assert times == sorted(times), f"Expected chronological order, got: {times}"


def test_high_priority_scheduled_before_low():
    """generate_plan() should schedule high-priority tasks before low-priority ones."""
    owner, pet, scheduler = make_scheduler(minutes=30)

    pet.add_task(Task("Low task",  10, "daily", "low"))
    pet.add_task(Task("High task", 10, "daily", "high"))

    scheduler.generate_plan()
    descriptions = [t.description for t in scheduler.planned_tasks]

    assert descriptions.index("High task") < descriptions.index("Low task")


def test_scheduler_does_not_exceed_time_budget():
    """generate_plan() should never schedule more minutes than available."""
    owner, pet, scheduler = make_scheduler(minutes=30)

    pet.add_task(Task("Task A", 20, "daily", "high"))
    pet.add_task(Task("Task B", 20, "daily", "high"))  # Together they exceed 30 min

    scheduler.generate_plan()

    assert scheduler.get_total_time() <= 30


# ---------- Recurrence Logic ----------

def test_daily_task_spawns_next_occurrence_after_completion():
    """Completing a daily task should add a new task due tomorrow."""
    owner, pet, scheduler = make_scheduler()

    pet.add_task(Task("Morning walk", 20, "daily", "high"))
    scheduler.generate_plan()
    scheduler.mark_task_complete("Morning walk")

    tomorrow = date.today() + timedelta(days=1)
    future_tasks = [t for t in pet.tasks if not t.completed]

    assert len(future_tasks) == 1, "Expected one new pending task after completion"
    assert future_tasks[0].next_due == tomorrow


def test_weekly_task_spawns_next_occurrence_in_7_days():
    """Completing a weekly task should add a new task due in 7 days."""
    owner, pet, scheduler = make_scheduler()

    pet.add_task(Task("Bath time", 30, "weekly", "low"))
    scheduler.generate_plan()
    scheduler.mark_task_complete("Bath time")

    next_week = date.today() + timedelta(days=7)
    future_tasks = [t for t in pet.tasks if not t.completed]

    assert len(future_tasks) == 1
    assert future_tasks[0].next_due == next_week


def test_as_needed_task_does_not_recur():
    """Completing an 'as needed' task should NOT spawn a new instance."""
    owner, pet, scheduler = make_scheduler()

    pet.add_task(Task("Vet visit", 60, "as needed", "high"))
    scheduler.generate_plan()
    scheduler.mark_task_complete("Vet visit")

    future_tasks = [t for t in pet.tasks if not t.completed]
    assert len(future_tasks) == 0, "as needed tasks should not auto-recur"


# ---------- Conflict Detection ----------

def test_conflict_detected_for_overlapping_tasks():
    """get_conflicts() should flag two tasks whose time ranges overlap."""
    owner, pet, scheduler = make_scheduler()

    # 08:00 + 20 min = ends 08:20 — overlaps with 08:10 start
    pet.add_task(Task("Morning walk",      20, "daily", "high",   start_time="08:00"))
    pet.add_task(Task("Administer inhaler", 5, "daily", "high",   start_time="08:10"))

    scheduler.generate_plan()
    conflicts = scheduler.get_conflicts()

    assert len(conflicts) > 0, "Expected at least one conflict to be reported"


def test_no_conflict_for_sequential_tasks():
    """get_conflicts() should return empty list when tasks do not overlap."""
    owner, pet, scheduler = make_scheduler()

    # 08:00 + 20 min = ends 08:20 — next starts at 08:30, no overlap
    pet.add_task(Task("Morning walk",   20, "daily", "high",   start_time="08:00"))
    pet.add_task(Task("Feed breakfast", 10, "daily", "high",   start_time="08:30"))

    scheduler.generate_plan()
    conflicts = scheduler.get_conflicts()

    assert conflicts == [], f"Expected no conflicts, got: {conflicts}"


# ---------- Edge Cases ----------

def test_pet_with_no_tasks_produces_empty_plan():
    """generate_plan() should return an empty list when a pet has no tasks."""
    owner, pet, scheduler = make_scheduler()
    # No tasks added
    scheduler.generate_plan()

    assert scheduler.planned_tasks == []


def test_owner_with_no_pets_returns_empty_task_list():
    """get_all_tasks() should return [] when owner has no pets."""
    owner = Owner("Jordan", 90)
    assert owner.get_all_tasks() == []


def test_task_larger_than_budget_is_skipped():
    """A task that exceeds available_minutes on its own should not be scheduled."""
    owner, pet, scheduler = make_scheduler(minutes=30)

    pet.add_task(Task("Long task", 60, "daily", "high"))  # 60 min > 30 min budget
    scheduler.generate_plan()

    assert scheduler.planned_tasks == []


def test_weekly_task_not_due_is_excluded():
    """A weekly task with next_due in the future should not appear in today's plan."""
    owner, pet, scheduler = make_scheduler()

    task = Task("Bath time", 30, "weekly", "low")
    task.next_due = date.today() + timedelta(days=3)  # Not due yet
    pet.add_task(task)

    scheduler.generate_plan()

    assert task not in scheduler.planned_tasks
