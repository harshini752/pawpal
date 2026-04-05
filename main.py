from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

# Setup
owner = Owner(name="Harshini")
dog = Pet(name="Bruno", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=2)

# Tasks - intentionally out of order
dog.add_task(Task(description="Medication", time="09:00", frequency="once", due_date=date.today()))
dog.add_task(Task(description="Morning Walk", time="07:00", frequency="daily", due_date=date.today()))
dog.add_task(Task(description="Feeding", time="08:00", frequency="daily", due_date=date.today()))

# Conflict task - same time as Feeding!
dog.add_task(Task(description="Bath Time", time="08:00", frequency="once", due_date=date.today()))

cat.add_task(Task(description="Feeding", time="08:30", frequency="daily", due_date=date.today()))

owner.add_pet(dog)
owner.add_pet(cat)
scheduler = Scheduler(owner)

# Print sorted schedule
print("=" * 40)
print("        🐾 TODAY'S SCHEDULE 🐾")
print("=" * 40)
sorted_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())
for pet, task in sorted_tasks:
    status = "✅" if task.is_complete else "❌"
    print(f"{status} [{task.time}] {pet.name} - {task.description} ({task.frequency})")

# Test conflict detection
print("\n--- Conflict Check ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(c)
else:
    print("✅ No conflicts found!")

# Test recurring task
print("\n--- Recurring Task Test ---")
print(f"Bruno's task count before: {len(dog.get_tasks())}")
scheduler.mark_task_complete("Bruno", "Morning Walk")
print(f"Bruno's task count after: {len(dog.get_tasks())}")
print("New task added for tomorrow:")
for task in dog.get_tasks():
    if not task.is_complete:
        print(f"  - {task.description} on {task.due_date}")
print("=" * 40)