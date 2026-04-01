import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart daily care planner for your pets.")

# --- Session State Initialization ---
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
    st.session_state.owner = Owner(owner_name, available_minutes)
    st.session_state.scheduler = None
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
        new_pet = Pet(pet_name, species, age)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {pet_name} the {species}!")

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

    col3, col4, col5, col6 = st.columns(4)
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
    with col5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col6:
        start_time = st.text_input("Start time (HH:MM)", value="", placeholder="e.g. 08:00")

    if st.button("Add Task"):
        target_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
        target_pet.add_task(Task(
            task_title, duration, frequency, priority,
            start_time=start_time if start_time.strip() else None
        ))
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
                    "Start time": t.start_time or "—",
                })
        st.table(rows)

st.divider()

# --- Section 4: Generate Schedule ---
st.subheader("4. Today's Schedule")

if st.session_state.owner is None or not st.session_state.owner.get_all_tasks():
    st.info("Add an owner, pets, and tasks before generating a schedule.")
else:
    if st.button("Generate Schedule"):
        st.session_state.scheduler = Scheduler(st.session_state.owner)
        st.session_state.scheduler.generate_plan()

    if st.session_state.scheduler and st.session_state.scheduler.planned_tasks:
        scheduler = st.session_state.scheduler

        # --- Time budget summary ---
        total = scheduler.get_total_time()
        remaining = scheduler.get_available_time()
        col1, col2, col3 = st.columns(3)
        col1.metric("Tasks scheduled", len(scheduler.planned_tasks))
        col2.metric("Time used (min)", total)
        col3.metric("Time remaining (min)", remaining)

        # --- Conflict warnings ---
        conflicts = scheduler.get_conflicts()
        if conflicts:
            st.warning("**Scheduling conflicts detected** — review before starting your day:")
            for c in conflicts:
                st.warning(c)
        else:
            st.success("No scheduling conflicts.")

        # --- View toggle: by priority or by time ---
        view = st.radio("View schedule by:", ["Priority order", "Time order"], horizontal=True)

        if view == "Time order":
            tasks_to_show = scheduler.sort_by_time()
        else:
            tasks_to_show = scheduler.planned_tasks

        rows = []
        for i, task in enumerate(tasks_to_show, 1):
            pet_name = next(p.name for p in st.session_state.owner.pets if task in p.tasks)
            rows.append({
                "#": i,
                "Pet": pet_name,
                "Task": task.description,
                "Start": task.start_time or "—",
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": "done" if task.completed else "pending",
            })
        st.table(rows)

        # --- Filter by pet ---
        st.write("**Filter by pet:**")
        pet_names = [p.name for p in st.session_state.owner.pets]
        selected = st.selectbox("Show tasks for", ["All pets"] + pet_names, key="filter_pet")

        if selected != "All pets":
            filtered = scheduler.get_tasks_for_pet(selected)
            if filtered:
                st.write(f"{len(filtered)} task(s) for {selected}:")
                for t in filtered:
                    st.write(f"- {t.get_summary()}")
            else:
                st.info(f"No planned tasks for {selected}.")
