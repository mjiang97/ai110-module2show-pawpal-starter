import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Task

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Macy")

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

owner = st.session_state.owner  # shorthand so we don't type session_state everywhere

# ---------------------------------------------------------------------------
# Section 1 — Add a Pet
# ---------------------------------------------------------------------------

st.subheader("Add a Pet")

with st.form("add_pet_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name")
        species  = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    with col2:
        age         = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
        care_needs  = st.text_input("Care needs (comma-separated)", placeholder="feeding x2, daily walk")

    if st.form_submit_button("Add Pet"):
        if pet_name.strip():
            needs_list = [c.strip() for c in care_needs.split(",") if c.strip()]
            owner.add_pet(pet_name.strip(), species, int(age), needs_list)
            st.success(f"{pet_name} added!")
        else:
            st.warning("Please enter a pet name.")

pets = owner.list_pets()
if pets:
    st.caption("Registered pets: " + ", ".join(p.name for p in pets))
else:
    st.info("No pets yet — add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Section 2 — Schedule a Task
# ---------------------------------------------------------------------------

st.subheader("Schedule a Task")

if not pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            pet_choice  = st.selectbox("Pet", [p.name for p in pets])
            task_type   = st.selectbox("Type", ["feeding", "walk", "medication", "appointment"])
            priority    = st.selectbox("Priority", ["high", "medium", "low"])
        with col2:
            description = st.text_input("Description", placeholder="Morning walk around the block")
            task_date   = st.date_input("Date", value=date.today())
            task_time   = st.time_input("Time")

        if st.form_submit_button("Add Task"):
            if description.strip():
                scheduled_at = datetime.combine(task_date, task_time)
                pet = owner.get_pet(pet_choice)
                pet.add_task(Task(
                    description=description.strip(),
                    scheduled_at=scheduled_at,
                    type=task_type,
                    priority=priority,
                ))
                st.success(f"Task scheduled for {pet_choice}!")
            else:
                st.warning("Please enter a task description.")

st.divider()

# ---------------------------------------------------------------------------
# Section 3 — Today's Schedule
# ---------------------------------------------------------------------------

st.subheader("Today's Schedule")

scheduler   = owner.scheduler
today_tasks = scheduler.sort_tasks_by_time(scheduler.get_today_tasks())

if not today_tasks:
    st.info("No tasks scheduled for today.")
else:
    for task in today_tasks:
        time_str = task.scheduled_at.strftime("%I:%M %p")
        col1, col2 = st.columns([5, 1])
        with col1:
            label = f"**[{time_str}]** `{task.priority.upper()}` — **{task.pet_name}**: {task.description}"
            if task.status == "completed":
                st.markdown(f"~~{label}~~")
            else:
                st.markdown(label)
        with col2:
            if task.status == "pending":
                if st.button("Done", key=task.id):
                    task.mark_completed()
                    st.rerun()
            else:
                st.markdown("✓")
