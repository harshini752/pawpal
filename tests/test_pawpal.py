from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, timedelta

# Test 1: Mark complete changes status
def test_mark_complete():
    task = Task(description="Walk", time="08:00", frequency="once")
    task.mark_complete()
    assert task.is_complete == True

# Test 2: Adding a task increases pet's task count
def test_add_task_increases_count():
    pet = Pet(name="Bruno", species="Dog", age=3)
    task = Task(description="Feeding", time="09:00", frequency="daily")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1

# Test 3: Sorting returns tasks in time order
def test_sort_by_time():
    owner = Owner(name="Harshini")
    pet = Pet(name="Bruno", species="Dog", age=3)
    pet.add_task(Task(description="Nap", time="12:00", frequency="once"))
    pet.add_task(Task(description="Walk", time="07:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks[0][1].time == "07:00"

# Test 4: Conflict detection catches duplicate times
def test_detect_conflicts():
    owner = Owner(name="Harshini")
    pet = Pet(name="Bruno", species="Dog", age=3)
    pet.add_task(Task(description="Walk", time="08:00", frequency="daily"))
    pet.add_task(Task(description="Feeding", time="08:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0

# Test 5: Daily recurring task creates next day task
def test_recurring_daily_task():
    owner = Owner(name="Harshini")
    pet = Pet(name="Bruno", species="Dog", age=3)
    today = date.today()
    pet.add_task(Task(description="Walk", time="07:00", 
                      frequency="daily", due_date=today))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Bruno", "Walk")
    dates = [t.due_date for t in pet.get_tasks()]
    assert today + timedelta(days=1) in dates

# Test 6: No conflict when times are different
def test_no_conflict():
    owner = Owner(name="Harshini")
    pet = Pet(name="Bruno", species="Dog", age=3)
    pet.add_task(Task(description="Walk", time="07:00", frequency="daily"))
    pet.add_task(Task(description="Feeding", time="08:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0