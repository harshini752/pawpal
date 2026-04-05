from dataclasses import dataclass, field
from typing import List
from datetime import date, timedelta

@dataclass
class Task:
    description: str
    time: str  # format "HH:MM"
    frequency: str  # "once", "daily", "weekly"
    is_complete: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark the task as complete and return next task if recurring."""
        self.is_complete = True
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1)
            )
        elif self.frequency == "weekly":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1)
            )
        return None

@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all pets as (pet, task) tuples."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet, task))
        return all_tasks

class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the Scheduler with an Owner."""
        self.owner = owner

    def get_todays_tasks(self):
        """Return all tasks due today."""
        today = date.today()
        return [(pet, task) for pet, task in self.owner.get_all_tasks()
                if task.due_date == today]

    def sort_by_time(self, tasks=None):
        """Sort tasks by their time attribute in HH:MM format."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda x: x[1].time)

    def filter_tasks(self, pet_name=None, completed=None):
        """Filter tasks by pet name or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name:
            tasks = [(p, t) for p, t in tasks if p.name == pet_name]
        if completed is not None:
            tasks = [(p, t) for p, t in tasks if t.is_complete == completed]
        return tasks

    def mark_task_complete(self, pet_name: str, task_description: str):
        """Mark a task complete and auto-schedule next if recurring."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                for task in pet.get_tasks():
                    if task.description == task_description and not task.is_complete:
                        next_task = task.mark_complete()
                        if next_task:
                            pet.add_task(next_task)
                        return True
        return False

    def detect_conflicts(self):
        """Detect tasks scheduled at the same time for the same pet."""
        conflicts = []
        for pet in self.owner.pets:
            seen_times = {}
            for task in pet.get_tasks():
                if task.time in seen_times:
                    conflicts.append(
                        f"⚠️ Conflict for {pet.name}: "
                        f"'{task.description}' and "
                        f"'{seen_times[task.time].description}' "
                        f"both at {task.time}"
                    )
                else:
                    seen_times[task.time] = task
        return conflicts