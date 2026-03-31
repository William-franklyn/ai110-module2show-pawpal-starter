from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup Owner ---
owner = Owner("Jordan", available_minutes=90)

# --- Setup Pets ---
mochi = Pet("Mochi", "dog", 3)
luna = Pet("Luna", "cat", 2, special_needs=["asthma inhaler"])

# --- Add Tasks to Mochi ---
mochi.add_task(Task("Morning walk", 20, "daily", "high"))
mochi.add_task(Task("Feed breakfast", 10, "daily", "high"))
mochi.add_task(Task("Play fetch", 25, "daily", "medium"))
mochi.add_task(Task("Bath time", 40, "weekly", "low"))

# --- Add Tasks to Luna ---
luna.add_task(Task("Administer inhaler", 5, "daily", "high"))
luna.add_task(Task("Clean litter box", 10, "daily", "medium"))
luna.add_task(Task("Brush fur", 15, "weekly", "low"))

# --- Register Pets with Owner ---
owner.add_pet(mochi)
owner.add_pet(luna)

# --- Run Scheduler ---
scheduler = Scheduler(owner)
scheduler.generate_plan()

# --- Print Today's Schedule ---
print("=" * 45)
print("         PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 45)
print(f"Owner : {owner.name}")
print(f"Pets  : {', '.join(p.name for p in owner.pets)}")
print(f"Budget: {owner.available_minutes} minutes")
print("-" * 45)

for i, task in enumerate(scheduler.planned_tasks, 1):
    pet_name = next(p.name for p in owner.pets if task in p.tasks)
    print(f"  {i}. [{pet_name}] {task.description} — {task.duration_minutes} min (priority: {task.priority})")

print("-" * 45)
print(f"  Total time used : {scheduler.get_total_time()} min")
print(f"  Time remaining  : {scheduler.get_available_time()} min")
print("=" * 45)
