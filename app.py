import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State Initialization ---
# Persists Owner and Scheduler across reruns so data isn't lost on every click.
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.divider()

# --- Section 1: Owner Setup ---
st.subheader("1. Owner Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)

if st.button("Set Owner"):
    # Creates a new Owner and stores it in session_state so it persists.
    st.session_state.owner = Owner(owner_name, available_minutes)
    st.session_state.scheduler = None  # Reset scheduler when owner changes
    st.success(f"Owner set: {owner_name} ({available_minutes} min available)")

st.divider()

# --- Section 2: Add a Pet ---
st.subheader("2. Add a Pet")

if st.session_state.owner is None:
    st.info("Set an owner first before adding pets.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

    if st.button("Add Pet"):
        # Calls owner.add_pet() — the Owner class handles storing the Pet.
        new_pet = Pet(pet_name, species, age)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet: {pet_name} the {species}")

    if st.session_state.owner.pets:
        st.write("**Current pets:**")
        for pet in st.session_state.owner.pets:
            st.write(f"- {pet.get_summary()}")

st.divider()

# --- Section 3: Add a Task ---
st.subheader("3. Add a Task")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]

    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Assign task to pet", pet_names)
    with col2:
        task_title = st.text_input("Task description", value="Morning walk")

    col3, col4, col5 = st.columns(3)
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
    with col5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add Task"):
        # Finds the right Pet object and calls pet.add_task() to attach the Task.
        target_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
        target_pet.add_task(Task(task_title, duration, frequency, priority))
        st.success(f"Added '{task_title}' to {selected_pet}")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All tasks:**")
        rows = []
        for pet in st.session_state.owner.pets:
            for t in pet.tasks:
                rows.append({
                    "Pet": pet.name,
                    "Task": t.description,
                    "Duration (min)": t.duration_minutes,
                    "Frequency": t.frequency,
                    "Priority": t.priority,
                })
        st.table(rows)

st.divider()

# --- Section 4: Generate Schedule ---
st.subheader("4. Generate Schedule")

if st.session_state.owner is None or not st.session_state.owner.get_all_tasks():
    st.info("Add an owner, pets, and tasks before generating a schedule.")
else:
    if st.button("Generate Schedule"):
        # Creates a Scheduler with the Owner, then calls generate_plan().
        st.session_state.scheduler = Scheduler(st.session_state.owner)
        st.session_state.scheduler.generate_plan()

    if st.session_state.scheduler and st.session_state.scheduler.planned_tasks:
        scheduler = st.session_state.scheduler
        st.success(f"Plan generated! {scheduler.get_total_time()} min scheduled, {scheduler.get_available_time()} min remaining.")

        rows = []
        for i, task in enumerate(scheduler.planned_tasks, 1):
            pet_name = next(p.name for p in st.session_state.owner.pets if task in p.tasks)
            rows.append({
                "#": i,
                "Pet": pet_name,
                "Task": task.description,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Status": "done" if task.completed else "pending",
            })
        st.table(rows)
