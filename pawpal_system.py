class Pet:
    """Represents a pet with basic profile information."""

    def __init__(self, name, species, age, special_needs=None):
        """
        Args:
            name: Pet's name.
            species: Type of animal (e.g. 'dog', 'cat', 'other').
            age: Pet's age in years.
            special_needs: Optional list of notes (e.g. allergies, medications).
        """
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs or []

    def get_summary(self):
        """Returns a readable description of the pet."""
        pass


class Owner:
    """Represents the pet owner and their scheduling constraints."""

    def __init__(self, name, available_minutes, preferences=None):
        """
        Args:
            name: Owner's name.
            available_minutes: Total time (in minutes) available for pet care today.
            preferences: Optional dict of scheduling preferences (e.g. {'prefers': 'morning'}).
        """
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}


class CareTask:
    """Represents a single pet care task to be scheduled."""

    def __init__(self, title, duration_minutes, priority, category, preferred_time=None):
        """
        Args:
            title: Short name for the task (e.g. 'Morning walk').
            duration_minutes: How long the task takes.
            priority: Importance level — 'low', 'medium', or 'high'.
            category: Type of care (e.g. 'walk', 'feeding', 'meds', 'grooming', 'enrichment').
            preferred_time: Optional time-of-day hint (e.g. 'morning', 'evening').
        """
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.preferred_time = preferred_time
        self.completed = False  # Tracks whether the task has been completed

    def is_high_priority(self):
        """Returns True if the task priority is 'high'."""
        pass

    def get_summary(self):
        """Returns a readable description of the task."""
        pass


class DailySchedule:
    """Builds and manages a daily care plan for a pet and owner pair."""

    def __init__(self, owner, pet, date=None):
        """
        Args:
            owner: Owner instance — provides time budget and preferences.
            pet: Pet instance — provides context for care needs.
            date: Optional date string for the schedule (e.g. '2026-03-31').
        """
        self.owner = owner
        self.pet = pet
        self.date = date
        self.tasks = []          # All tasks available to be scheduled
        self.planned_tasks = []  # Ordered tasks selected for the day's plan

    def add_task(self, task):
        """Adds a CareTask to the pool of tasks to consider."""
        pass

    def remove_task(self, title):
        """Removes a task from the pool by its title."""
        pass

    def generate_plan(self):
        """Selects and orders tasks by priority within the owner's time budget."""
        pass

    def explain_plan(self):
        """Returns a string explaining why each task was chosen and when it occurs."""
        pass

    def get_available_time(self):
        """Returns remaining time after subtracting planned task durations from owner's budget."""
        pass

    def get_total_time(self):
        """Returns the total duration (in minutes) of all planned tasks."""
        pass
