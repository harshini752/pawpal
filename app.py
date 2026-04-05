import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.markdown("*Your smart pet care management system*")

# ── Session State Setup ──────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Harshini")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# ── Add a Pet ────────────────────────────────────────────────────
st.divider()
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
        existing = [p.name for p in owner.pets]
        if pet_name in existing:
            st.warning(f"⚠️ {pet_name} is already added!")
        else:
            owner.add_pet(Pet(name=pet_name, species=species, age=age))
            st.success(f"✅ {pet_name} the {species} added!")
    else:
        st.warning("Please enter a pet name.")

# Show current pets
if owner.pets:
    st.markdown("**Your pets:** " + 
                ", ".join([f"🐾 {p.name}" for p in owner.pets]))

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
        if task_desc and task_time:
            pet = next(p for p in owner.pets if p.name == selected_pet)
            pet.add_task(Task(
                description=task_desc,
                time=task_time,
                frequency=frequency,
                due_date=date.today()
            ))
            st.success(f"✅ '{task_desc}' scheduled for {selected_pet} at {task_time}!")
        else:
            st.warning("Please fill in all task fields.")
else:
    st.info("👆 Add a pet first before scheduling tasks.")

# ── Today's Schedule ─────────────────────────────────────────────
st.divider()
st.subheader("📅 Today's Schedule")

if st.button("Generate Schedule"):
    todays_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())

    if todays_tasks:
        st.markdown("### Tasks for Today")
        for pet, task in todays_tasks:
            status = "✅" if task.is_complete else "❌"
            freq_badge = f"`{task.frequency}`"
            st.write(
                f"{status} **[{task.time}]** "
                f"{pet.name} — {task.description} {freq_badge}"
            )
    else:
        st.info("No tasks scheduled for today. Add some tasks above!")

    # Conflict Warnings
    st.divider()
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.markdown("### ⚠️ Scheduling Conflicts")
        for c in conflicts:
            st.warning(c)
    else:
        st.success("✅ No scheduling conflicts found!")

# ── Mark Task Complete ───────────────────────────────────────────
st.divider()
st.subheader("✅ Mark Task Complete")

if owner.pets:
    col1, col2 = st.columns(2)
    with col1:
        complete_pet = st.selectbox("Pet", pet_names, key="complete_pet")
    with col2:
        pet_tasks = [t.description for p in owner.pets 
                     if p.name == complete_pet 
                     for t in p.get_tasks() if not t.is_complete]
        if pet_tasks:
            complete_task = st.selectbox("Task", pet_tasks)
            if st.button("Mark Complete"):
                success = scheduler.mark_task_complete(complete_pet, complete_task)
                if success:
                    st.success(f"✅ '{complete_task}' marked complete!")
                    st.info("🔄 Recurring task auto-scheduled for next occurrence!")
        else:
            st.info("No pending tasks for this pet.")
else:
    st.info("Add a pet first.")