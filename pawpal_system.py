from datetime import date, timedelta
from itertools import combinations


class Task:
    """Represents a single pet care activity."""

    def __init__(self, description, duration_minutes, frequency, priority="medium", preferred_time=None, start_time=None):
        """
        Args:
            description: What the task is (e.g. 'Morning walk').
            duration_minutes: How long the task takes.
            frequency: How often it occurs — 'daily', 'weekly', or 'as needed'.
            priority: 'low', 'medium', or 'high'.
            preferred_time: Optional time-of-day hint — 'morning', 'afternoon', 'evening'.
            start_time: Optional scheduled start time in 'HH:MM' format (e.g. '08:00').
        """
        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency
        self.priority = priority
        self.preferred_time = preferred_time
        self.start_time = start_time  # 'HH:MM' format for time-based sorting
        self.completed = False
        self.last_scheduled = None  # Tracks the last date this task was scheduled
        self.next_due = date.today()  # The date this task is next due

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Resets the task to incomplete."""
        self.completed = False

    def is_high_priority(self):
        """Returns True if priority is 'high'."""
        return self.priority == "high"

    def is_due_today(self):
        """Returns True if next_due is today or in the past."""
        return self.next_due <= date.today()

    def get_summary(self):
        """Returns a readable one-line summary of the task."""
        status = "done" if self.completed else "pending"
        time_hint = f", {self.preferred_time}" if self.preferred_time else ""
        return f"[{status}] {self.description} ({self.duration_minutes} min, {self.frequency}{time_hint}, priority: {self.priority})"


class Pet:
    """Represents a pet and its list of care tasks."""

    def __init__(self, name, species, age, special_needs=None):
        """
        Args:
            name: Pet's name.
            species: Type of animal (e.g. 'dog', 'cat').
            age: Pet's age in years.
            special_needs: Optional list of notes (e.g. allergies, medications).
        """
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs or []
        self.tasks = []

    def add_task(self, task):
        """Adds a Task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, description):
        """Removes a task by its description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_pending_tasks(self):
        """Returns all incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.completed]

    def get_summary(self):
        """Returns a readable description of the pet."""
        needs = ", ".join(self.special_needs) if self.special_needs else "none"
        return f"{self.name} ({self.species}, age {self.age}) — special needs: {needs}"


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name, available_minutes, preferences=None):
        """
        Args:
            name: Owner's name.
            available_minutes: Total time (in minutes) available for pet care today.
            preferences: Optional dict of scheduling preferences.
        """
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}
        self.pets = []

    def add_pet(self, pet):
        """Adds a Pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, name):
        """Removes a pet by name."""
        self.pets = [p for p in self.pets if p.name != name]

    def get_all_tasks(self):
        """Returns all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_all_pending_tasks(self):
        """Returns all incomplete tasks across all pets."""
        return [t for t in self.get_all_tasks() if not t.completed]


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an owner's pets."""

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
    TIME_ORDER = {"morning": 0, "afternoon": 1, "evening": 2, None: 3}

    def __init__(self, owner):
        """
        Args:
            owner: Owner instance to pull pets and tasks from.
        """
        self.owner = owner
        self.planned_tasks = []

    def generate_plan(self):
        """
        Builds a daily plan from tasks that are due today, sorted by priority,
        then preferred time, then shortest duration. Skips duplicates and tasks
        not due based on their recurrence frequency.
        """
        pending = [t for t in self.owner.get_all_pending_tasks() if t.is_due_today()]

        # Sort by: priority → preferred time slot → shortest duration (fits more tasks)
        sorted_tasks = sorted(
            pending,
            key=lambda t: (
                self.PRIORITY_ORDER.get(t.priority, 1),
                self.TIME_ORDER.get(t.preferred_time, 3),
                t.duration_minutes,
            ),
        )

        self.planned_tasks = []
        time_used = 0

        for task in sorted_tasks:
            if self._is_duplicate(task):
                continue
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                self.planned_tasks.append(task)
                task.last_scheduled = date.today()
                time_used += task.duration_minutes

        return self.planned_tasks

    @staticmethod
    def _to_minutes(start_time):
        """Converts 'HH:MM' string to total minutes since midnight."""
        h, m = start_time.split(":")
        return int(h) * 60 + int(m)

    def get_conflicts(self):
        """
        Detects tasks whose time ranges overlap (start_time + duration).
        Returns a list of warning strings — never raises an exception.
        Tasks without a start_time are skipped.
        """
        timed = [t for t in self.planned_tasks if t.start_time is not None]
        warnings = []

        for a, b in combinations(timed, 2):
            a_start = self._to_minutes(a.start_time)
            b_start = self._to_minutes(b.start_time)

            # Overlap when one starts before the other ends
            if a_start < b_start + b.duration_minutes and b_start < a_start + a.duration_minutes:
                a_pet = next((p.name for p in self.owner.pets if a in p.tasks), "?")
                b_pet = next((p.name for p in self.owner.pets if b in p.tasks), "?")
                warnings.append(
                    f"CONFLICT: [{a_pet}] '{a.description}' ({a.start_time}, {a.duration_minutes} min) "
                    f"overlaps with [{b_pet}] '{b.description}' ({b.start_time}, {b.duration_minutes} min)"
                )

        return warnings

    def _is_duplicate(self, task):
        """Returns True if a task with the same description is already in the plan."""
        return any(t.description == task.description for t in self.planned_tasks)

    def sort_by_time(self):
        """Returns planned tasks sorted by start_time ('HH:MM'). Tasks without a start_time appear last."""
        return sorted(
            self.planned_tasks,
            key=lambda t: t.start_time if t.start_time is not None else "99:99",
        )

    def get_tasks_for_pet(self, pet_name):
        """Returns all planned tasks assigned to a specific pet."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return [t for t in self.planned_tasks if t in pet.tasks]
        return []

    def get_completed_tasks(self):
        """Returns all completed tasks from the plan."""
        return [t for t in self.planned_tasks if t.completed]

    def get_pending_tasks(self):
        """Returns all incomplete tasks from the plan."""
        return [t for t in self.planned_tasks if not t.completed]

    def get_total_time(self):
        """Returns total duration (in minutes) of all planned tasks."""
        return sum(t.duration_minutes for t in self.planned_tasks)

    def get_available_time(self):
        """Returns remaining time after planned tasks."""
        return self.owner.available_minutes - self.get_total_time()

    def explain_plan(self):
        """Returns a string explaining the planned tasks and why they were chosen."""
        if not self.planned_tasks:
            return "No tasks were scheduled. Run generate_plan() first or add tasks."

        lines = [
            f"Daily plan for {self.owner.name} "
            f"({self.get_total_time()} min used, {self.get_available_time()} min remaining):\n"
        ]

        for i, task in enumerate(self.planned_tasks, 1):
            pet_name = next(p.name for p in self.owner.pets if task in p.tasks)
            lines.append(f"  {i}. [{pet_name}] {task.get_summary()}")

        return "\n".join(lines)

    def mark_task_complete(self, description):
        """
        Marks a planned task complete and automatically schedules the next occurrence.
        - 'daily' tasks: next due tomorrow (today + 1 day via timedelta)
        - 'weekly' tasks: next due in 7 days (today + 7 days via timedelta)
        - 'as needed' tasks: no automatic recurrence
        """
        for task in self.planned_tasks:
            if task.description == description:
                task.mark_complete()
                task.last_scheduled = date.today()

                # Spawn the next occurrence based on frequency
                if task.frequency == "daily":
                    next_task = Task(
                        task.description,
                        task.duration_minutes,
                        task.frequency,
                        task.priority,
                        task.preferred_time,
                        task.start_time,
                    )
                    next_task.next_due = date.today() + timedelta(days=1)

                    # Add to the same pet's task list
                    for pet in self.owner.pets:
                        if task in pet.tasks:
                            pet.add_task(next_task)
                            break

                elif task.frequency == "weekly":
                    next_task = Task(
                        task.description,
                        task.duration_minutes,
                        task.frequency,
                        task.priority,
                        task.preferred_time,
                        task.start_time,
                    )
                    next_task.next_due = date.today() + timedelta(days=7)

                    for pet in self.owner.pets:
                        if task in pet.tasks:
                            pet.add_task(next_task)
                            break

                return True
        return False
