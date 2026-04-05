from dataclasses import dataclass, field
from typing import List
from datetime import date

@dataclass
class Task:
    description: str
    time: str  # format "HH:MM"
    frequency: str  # "once", "daily", "weekly"
    is_complete: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        pass

@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_tasks(self):
        pass

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def get_all_tasks(self):
        pass

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_tasks(self):
        pass

    def sort_by_time(self):
        pass

    def filter_tasks(self, pet_name=None, completed=None):
        pass

    def detect_conflicts(self):
        pass