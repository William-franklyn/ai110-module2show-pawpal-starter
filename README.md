# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner stay consistent with daily pet care. You enter your pets, add care tasks, and the app builds a smart daily schedule based on your available time, task priorities, and preferred time slots.

---

## Features

- **Priority-based scheduling** — the scheduler always places high-priority tasks first (medications, feeding), then medium, then low. Within the same priority level, shorter tasks are scheduled first to fit as many tasks as possible into the available time budget.

- **Sorting by time** — once a plan is generated, you can switch to a time-ordered view that sorts tasks chronologically by their scheduled start time (HH:MM format), so you see your day laid out in order.

- **Conflict detection** — if two tasks overlap in time (e.g. a 20-minute walk starting at 08:00 and an inhaler at 08:10), the app flags it as a warning before you start your day, rather than silently ignoring it.

- **Recurring task automation** — marking a daily task complete automatically creates the next occurrence due tomorrow. Weekly tasks reappear in 7 days. "As needed" tasks don't recur automatically.

- **Filtering by pet** — when you have multiple pets, you can filter the schedule to see only the tasks belonging to a specific pet.

- **Time budget tracking** — the app shows how many minutes are scheduled vs. how many are still available, so you always know if your plan is realistic.

- **Multi-pet support** — one owner can manage multiple pets, each with their own independent task lists.

---

## 📸 Demo

<a href="app_pic2.png" target="_blank"><img src='app_pic2.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>
<a href="app_pic1.png" target="_blank"><img src='app_pic1.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the demo script

```bash
python main.py
```

---

## Testing PawPal+

To run the tests, make sure you're inside the project folder and run:

```bash
python -m pytest tests/ -v
```

I wrote 14 tests total covering the parts of the system I was most worried about breaking. The main things I tested were whether the scheduler actually respects the time budget, whether high-priority tasks end up before low-priority ones, and whether completing a daily or weekly task correctly creates a new one for the next day or next week. I also added a few edge cases like what happens when a pet has no tasks, or when a single task is longer than the entire time budget — both of these used to silently do nothing, so I wanted to make sure they still returned cleanly without crashing.

The conflict detection tests were important too — I wanted to make sure two tasks starting at overlapping times would get flagged, but tasks that run back-to-back wouldn't be falsely reported as conflicts.

**All 14 tests passed** — screenshot below as evidence:

![Test results](Capture.PNG)

**Confidence level: 4/5**

I'm pretty confident the scheduling logic and recurrence work correctly. The main thing I'm not fully sure about yet is the Streamlit UI layer — I haven't written any automated tests for that side, so there could still be edge cases in how the app handles user input. That would be the next thing to tackle.

---

## Smarter Scheduling

The scheduler goes beyond a simple priority list. Key features:

- **Priority + duration sorting** — tasks are sorted high → medium → low priority; within the same priority, shorter tasks are scheduled first to fit more into the time budget.
- **Preferred time slots** — tasks tagged `morning`, `afternoon`, or `evening` are ordered within their priority group accordingly.
- **Recurring task automation** — when a `daily` task is marked complete, a new instance is automatically created due tomorrow (`today + timedelta(days=1)`). Weekly tasks recur in 7 days.
- **Filtering** — filter planned tasks by pet name, completion status (pending/done), or view all.
- **Conflict detection** — `get_conflicts()` checks every pair of timed tasks for overlapping time ranges and returns human-readable warnings without crashing the app.

---

## Suggested Workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
