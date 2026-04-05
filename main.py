from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

# Create Owner
owner = Owner(name="Harshini")

# Create Pets
dog = Pet(name="Bruno", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=2)

# Create Tasks for Bruno
dog.add_task(Task(description="Morning Walk", time="07:00", frequency="daily", due_date=date.today()))
dog.add_task(Task(description="Feeding", time="08:00", frequency="daily", due_date=date.today()))
dog.add_task(Task(description="Medication", time="09:00", frequency="once", due_date=date.today()))

# Create Tasks for Whiskers
cat.add_task(Task(description="Feeding", time="08:30", frequency="daily", due_date=date.today()))
cat.add_task(Task(description="Vet Appointment", time="11:00", frequency="once", due_date=date.today()))

# Add Pets to Owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create Scheduler
scheduler = Scheduler(owner)

# Print Today's Schedule
print("=" * 40)
print("        🐾 TODAY'S SCHEDULE 🐾")
print("=" * 40)

sorted_tasks = scheduler.sort_by_time()
for pet, task in sorted_tasks:
    status = "✅" if task.is_complete else "❌"
    print(f"{status} [{task.time}] {pet.name} - {task.description} ({task.frequency})")

# Check for Conflicts
print("\n--- Conflict Check ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(c)
else:
    print("✅ No conflicts found!")

print("=" * 40)