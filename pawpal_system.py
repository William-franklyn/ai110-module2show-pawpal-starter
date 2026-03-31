class Task:
    """Represents a single pet care activity."""

    def __init__(self, description, duration_minutes, frequency, priority="medium"):
        """
        Args:
            description: What the task is (e.g. 'Morning walk').
            duration_minutes: How long the task takes.
            frequency: How often it occurs (e.g. 'daily', 'weekly').
            priority: 'low', 'medium', or 'high'.
        """
        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency
        self.priority = priority
        self.completed = False

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Resets the task to incomplete."""
        self.completed = False

    def is_high_priority(self):
        """Returns True if priority is 'high'."""
        return self.priority == "high"

    def get_summary(self):
        """Returns a readable one-line summary of the task."""
        status = "done" if self.completed else "pending"
        return f"[{status}] {self.description} ({self.duration_minutes} min, {self.frequency}, priority: {self.priority})"


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

    def __init__(self, owner):
        """
        Args:
            owner: Owner instance to pull pets and tasks from.
        """
        self.owner = owner
        self.planned_tasks = []

    def generate_plan(self):
        """
        Builds a daily plan by selecting pending tasks sorted by priority,
        fitting as many as possible within the owner's available time budget.
        """
        pending = self.owner.get_all_pending_tasks()
        sorted_tasks = sorted(pending, key=lambda t: self.PRIORITY_ORDER.get(t.priority, 1))

        self.planned_tasks = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                self.planned_tasks.append(task)
                time_used += task.duration_minutes

        return self.planned_tasks

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

        lines = [f"Daily plan for {self.owner.name} ({self.get_total_time()} min used, "
                 f"{self.get_available_time()} min remaining):\n"]

        for i, task in enumerate(self.planned_tasks, 1):
            lines.append(f"  {i}. {task.get_summary()}")

        return "\n".join(lines)

    def mark_task_complete(self, description):
        """Marks a planned task complete by its description."""
        for task in self.planned_tasks:
            if task.description == description:
                task.mark_complete()
                return True
        return False
