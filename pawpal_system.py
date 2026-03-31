class Pet:
    def __init__(self, name, species, age, special_needs=None):
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs or []

    def get_summary(self):
        pass


class Owner:
    def __init__(self, name, available_minutes, preferences=None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}

    def get_available_time(self):
        pass


class CareTask:
    def __init__(self, title, duration_minutes, priority, category, preferred_time=None):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.preferred_time = preferred_time

    def is_high_priority(self):
        pass

    def get_summary(self):
        pass


class DailySchedule:
    def __init__(self, owner, pet):
        self.owner = owner
        self.pet = pet
        self.tasks = []
        self.planned_tasks = []

    def add_task(self, task):
        pass

    def remove_task(self, title):
        pass

    def generate_plan(self):
        pass

    def explain_plan(self):
        pass

    def get_total_time(self):
        pass
