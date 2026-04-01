from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup Owner ---
owner = Owner("Jordan", available_minutes=120)

# --- Setup Pets ---
mochi = Pet("Mochi", "dog", 3)
luna = Pet("Luna", "cat", 2, special_needs=["asthma inhaler"])

# --- Add Tasks (two intentional overlaps for conflict detection) ---
# Overlap 1: Mochi's Morning walk (08:00, 20 min → ends 08:20)
#            Luna's Administer inhaler (08:10, 5 min → ends 08:15)  ← overlaps
# Overlap 2: Mochi's Play fetch (15:00, 25 min → ends 15:25)
#            Luna's Brush fur (15:15, 15 min → ends 15:30)          ← overlaps
mochi.add_task(Task("Play fetch",       25, "daily",  "medium", start_time="15:00"))
mochi.add_task(Task("Morning walk",     20, "daily",  "high",   start_time="08:00"))
mochi.add_task(Task("Evening walk",     20, "daily",  "medium", start_time="18:30"))
mochi.add_task(Task("Feed breakfast",   10, "daily",  "high",   start_time="07:30"))
mochi.add_task(Task("Bath time",        40, "weekly", "low",    start_time="11:00"))

luna.add_task(Task("Administer inhaler", 5, "daily",  "high",   start_time="08:10"))  # overlaps Morning walk
luna.add_task(Task("Brush fur",         15, "weekly", "low",    start_time="15:15"))  # overlaps Play fetch
luna.add_task(Task("Clean litter box",  10, "daily",  "medium", start_time="09:00"))

# --- Register Pets ---
owner.add_pet(mochi)
owner.add_pet(luna)

# --- Run Scheduler ---
scheduler = Scheduler(owner)
scheduler.generate_plan()

# --- Print: Sorted by Priority (default plan) ---
print("=" * 50)
print("     PAWPAL+ — PRIORITY-BASED PLAN")
print("=" * 50)
for i, task in enumerate(scheduler.planned_tasks, 1):
    pet_name = next(p.name for p in owner.pets if task in p.tasks)
    print(f"  {i}. [{pet_name}] {task.description} — {task.duration_minutes} min (priority: {task.priority})")

# --- Print: Sorted by Time (HH:MM) ---
print()
print("=" * 50)
print("     PAWPAL+ — TIME-ORDERED SCHEDULE")
print("=" * 50)
for i, task in enumerate(scheduler.sort_by_time(), 1):
    pet_name = next(p.name for p in owner.pets if task in p.tasks)
    time = task.start_time or "no time set"
    print(f"  {i}. {time} [{pet_name}] {task.description} — {task.duration_minutes} min")

# --- Print: Filter by Pet ---
print()
print("=" * 50)
print("     FILTER: Mochi's Tasks Only")
print("=" * 50)
for task in scheduler.get_tasks_for_pet("Mochi"):
    print(f"  - {task.description} ({task.priority})")

# --- Mark one complete, then filter by status ---
scheduler.mark_task_complete("Morning walk")
scheduler.mark_task_complete("Administer inhaler")

print()
print("=" * 50)
print("     FILTER: Completed Tasks")
print("=" * 50)
for task in scheduler.get_completed_tasks():
    print(f"  - {task.description}")

print()
print("=" * 50)
print("     FILTER: Still Pending")
print("=" * 50)
for task in scheduler.get_pending_tasks():
    print(f"  - {task.description}")

print()
print(f"  Time used: {scheduler.get_total_time()} min | Remaining: {scheduler.get_available_time()} min")
print("=" * 50)

# --- Conflict Detection ---
print()
print("=" * 50)
print("     CONFLICT CHECK")
print("=" * 50)
conflicts = scheduler.get_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts detected.")
print("=" * 50)
