# PawPal+ Project Reflection

## 1. System Design
For Pawpal project, I identified three main activities to be performed by the app, 
1. Let a user enter basic owner + pet info
2. Let a user add/edit tasks (duration + priority at minimum)
3. Generate a daily schedule/plan based on constraints and priorities
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Pet
Attributes: name, species, age, special_needs
Methods: get_summary()

Owner
Attributes: name, available_minutes, preferences
Methods: get_available_time()

CareTask
Attributes: title, duration_minutes, priority, category, preferred_time
Methods: is_high_priority(), get_summary()

DailySchedule
Attributes: owner, pet, tasks, planned_tasks
Methods: add_task(), remove_task(), generate_plan(), explain_plan(), get_total_time()

**b. Design changes**

- Did your design change during implementation?
Not yet, but maybe as i keepdoing it i will make changes, if necessary.

- If yes, describe at least one change and why you made it.
The only thing is that the AI generated another class for thescheduler which didn't make sense so i removed it.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a **greedy algorithm** — it picks tasks in priority order and adds each one if it fits within the remaining time budget. This means it does not backtrack. For example, if a 40-minute low-priority task is skipped because only 35 minutes remain, the scheduler will not go back and swap out an earlier medium-priority task to make room for it.

This is a reasonable tradeoff for a daily pet care app because the number of tasks is small (typically under 20), so an optimal solution is not worth the added complexity. The greedy approach is fast, predictable, and easy to explain to the user — "high priority tasks always get scheduled first." A full optimization (e.g. dynamic programming knapsack) would be harder to debug and overkill for this use case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
