# PawPal+ Project Reflection

## 1. System Design

For the PawPal+ project, I identified three main activities to be performed by the app:
1. Let a user enter basic owner + pet info
2. Let a user add/edit tasks (duration + priority at minimum)
3. Generate a daily schedule/plan based on constraints and priorities

**a. Initial design**

My initial UML had four classes: Pet, Owner, CareTask, and DailySchedule. Pet stored the animal's basic info and a list of tasks. Owner held the person's name and how much time they had available. CareTask represented a single activity with a title, duration, priority, category, and optional time hint. DailySchedule was the central object that tied everything together — it held references to both the owner and the pet and was responsible for generating and explaining the plan.

**b. Design changes**

The design changed quite a bit during implementation. The most significant change was replacing DailySchedule with a proper Scheduler class, and restructuring the ownership hierarchy so that Owner holds a list of Pets, and each Pet holds its own tasks. In the original design, tasks lived inside DailySchedule, which made it awkward to support multiple pets. Moving tasks into Pet and letting Scheduler pull from the Owner made the flow much more natural.

CareTask was also renamed to Task and gained several new attributes — start_time for time-based sorting, next_due for recurrence tracking, and last_scheduled for weekly frequency logic. None of these were in the initial design; they came up as I built the actual scheduling logic and realized I needed them.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints: time budget (available_minutes from the Owner), task priority (high / medium / low), and recurrence (is the task actually due today based on its frequency and next_due date). I decided priority mattered most because from a pet care perspective, medications and feeding should never get bumped in favor of a bath or playtime. Time budget came second — the app should be realistic and never schedule more than the owner can actually do. Recurrence was the last piece added, mainly to avoid scheduling a weekly task every day.

**b. Tradeoffs**

The scheduler uses a greedy algorithm — it picks tasks in priority order and adds each one if it fits within the remaining time budget. This means it does not backtrack. For example, if a 40-minute low-priority task is skipped because only 35 minutes remain, the scheduler will not go back and swap out an earlier medium-priority task to make room for it.

This is a reasonable tradeoff for a daily pet care app because the number of tasks is small (typically under 20), so an optimal solution is not worth the added complexity. The greedy approach is fast, predictable, and easy to explain to the user — "high priority tasks always get scheduled first." A full optimization like a dynamic programming knapsack would be harder to debug and overkill for this use case.

---

## 3. AI Collaboration

**a. How I used AI**

I used AI throughout the whole project but in different ways at each phase. In the design phase it helped me brainstorm what classes I needed and what attributes made sense. In the implementation phase I used it to write the initial stubs and then flesh out the logic — things like the sorting key using a lambda, the itertools.combinations refactor for conflict detection, and the timedelta math for recurrence. In the testing phase it helped me think through edge cases I hadn't considered, like what should happen when a pet has no tasks or when a task is larger than the entire time budget.

The most useful type of prompt was giving it a specific problem and asking for a focused solution — for example "how should sort() handle tasks with no start_time so they appear last?" That got much better results than open-ended questions like "improve my scheduler."

**b. Judgment and verification**

One clear moment was early in the project when the AI suggested adding a Scheduler class as a separate object right from the start. At the time that felt unnecessary — the DailySchedule class already existed and I thought it could handle everything. So I removed it and kept the original four-class design. That turned out to be wrong; as the project grew and I added multi-pet support and sorting and conflict detection, the logic got too heavy for DailySchedule and I ended up adding a Scheduler anyway. The AI was right, I just wasn't ready to see why yet. That was a useful lesson — sometimes the suggestion makes sense once you've built enough to understand the problem it's solving.

---

## 4. Testing and Verification

**a. What I tested**

I wrote 14 tests covering: task completion status, pet task count after adding tasks, chronological sorting, priority ordering in the plan, time budget enforcement, daily and weekly recurrence spawning the correct next_due date, as-needed tasks not recurring, conflict detection for overlapping and sequential tasks, and edge cases like empty pets, no pets, oversized tasks, and weekly tasks that aren't due yet.

These tests mattered because the scheduler has several moving parts — if the sorting logic breaks, or if recurrence creates a task with the wrong date, it wouldn't be obvious just by running the app manually. Having the tests meant I could refactor things like get_conflicts() with confidence.

**b. Confidence**

I'd say 4 out of 5. The core scheduling logic is well tested and I'm confident it works correctly. The part I'm less sure about is the Streamlit UI — I haven't written automated tests for it, so there could be edge cases in how the app handles user input (like entering an invalid time format or leaving fields blank) that I haven't caught yet.

---

## 5. Reflection

**a. What went well**

The part I'm most satisfied with is the conflict detection. It started as a simple idea — just check if two tasks overlap — but the implementation ended up being clean and genuinely useful. Using itertools.combinations to generate all pairs, converting HH:MM to minutes for the math, and returning warnings as plain strings instead of raising exceptions all felt like the right decisions. It's one of those features that doesn't feel bolted on.

**b. What I would improve**

If I had another iteration I would add conflict resolution, not just detection. Right now the app tells you two tasks overlap but doesn't suggest how to fix it — it would be more helpful to automatically shift one task's start time or flag it and ask the owner which one to move. I'd also add a way to mark tasks complete directly in the Streamlit UI rather than only through code.

**c. Key takeaway**

The biggest thing I learned is that AI is most useful when you already have a clear picture of what you're building. When I gave it a specific problem with context — here's my class, here's what I want this method to do — the output was good and fast. When I was vague or didn't understand the problem myself, the suggestions were generic and sometimes pointed me in the wrong direction. Being the "lead architect" meant I had to do enough thinking first so that I could actually evaluate what the AI was giving me. The tool works best as a collaborator, not a replacement for understanding the problem.
