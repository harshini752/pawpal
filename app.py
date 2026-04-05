import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session State Setup ──────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Harshini")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# ── Add a Pet ────────────────────────────────────────────────────
st.subheader("🐶 Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet Name")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    if pet_name:
        owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"✅ {pet_name} added!")
    else:
        st.warning("Please enter a pet name.")

# ── Add a Task ───────────────────────────────────────────────────
st.divider()
st.subheader("📋 Schedule a Task")

pet_names = [p.name for p in owner.pets]
if pet_names:
    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Select Pet", pet_names)
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")

    col3, col4 = st.columns(2)
    with col3:
        task_desc = st.text_input("Task Description", value="Morning Walk")
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        pet = next(p for p in owner.pets if p.name == selected_pet)
        pet.add_task(Task(
            description=task_desc,
            time=task_time,
            frequency=frequency,
            due_date=date.today()
        ))
        st.success(f"✅ Task '{task_desc}' added for {selected_pet}!")
else:
    st.info("Add a pet first before scheduling tasks.")

# ── Today's Schedule ─────────────────────────────────────────────
st.divider()
st.subheader("📅 Today's Schedule")

if st.button("Generate Schedule"):
    todays_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())

    if todays_tasks:
        for pet, task in todays_tasks:
            status = "✅" if task.is_complete else "❌"
            st.write(f"{status} **[{task.time}]** {pet.name} — {task.description} `({task.frequency})`")
    else:
        st.info("No tasks scheduled for today.")

    # Conflict Check
    st.divider()
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            st.warning(c)
    else:
        st.success("✅ No conflicts found!")