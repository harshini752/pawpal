# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
1. Add a pet to the system
2. Schedule a task ( feeding, walk, medication) for a pet
3. View all tasks scheduled for today 
- What classes did you include, and what responsibilities did you assign to each?
I designed 4 classes:

- Task: holds activity details like description, time, 
  frequency, and completion status. Uses Python dataclass 
  for clean structure.

- Pet: holds pet info (name, species, age) and owns a 
  list of Task objects. Can add and retrieve tasks.

- Owner: manages multiple Pet objects and can retrieve 
  all tasks across all pets.

- Scheduler: the "brain" that takes an Owner and handles 
  sorting, filtering, and conflict detection of tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
No major changes yet. The initial design matches the UML 
diagram closely. The Scheduler was kept as a separate class 
rather than combining it with Owner to keep responsibilities 
clean and modular.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler considers time as the main constraint, 
sorting all tasks chronologically using HH:MM format. 
Time was prioritized because pet care tasks like feeding 
and medication are time-sensitive.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The conflict detection only checks for exact time matches, 
not overlapping durations. For example, a 30-minute walk 
starting at 08:00 and a task at 08:15 would not be flagged. 
This is reasonable for a simple scheduler but would need 
duration tracking in a more advanced version.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI to help generate class skeletons from my UML 
design, scaffold the full implementation, suggest test 
cases, and debug logic. The most helpful prompts were 
specific ones like "generate a conflict detection method 
that returns warnings instead of crashing."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
When AI suggested combining Owner and Scheduler into one 
class, I rejected it because keeping them separate follows 
the Single Responsibility Principle and makes the code 
easier to test and maintain.

---

## 4. Testing and Verification

**a. What you tested**

I tested 6 behaviors:
- mark_complete() correctly changes task status to True
- Adding a task to a Pet increases its task count
- sort_by_time() returns tasks in chronological order
- detect_conflicts() correctly flags two tasks at same time
- Daily recurring tasks auto-schedule for the next day
- No false conflict warnings when times are different

These tests are important because they verify the core 
logic the entire app depends on.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence:(4/5)
All 6 tests pass. The system handles happy paths and key 
edge cases well. Next I would test empty pet lists, invalid 
time formats like "25:00", and weekly recurring tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with the algorithmic layer — sorting, 
conflict detection, and recurring tasks all work correctly 
and are verified by automated tests.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would add duration to tasks so conflict detection can 
catch overlapping time windows, not just exact matches. 
I would also add data persistence so pets and tasks are 
saved between sessions.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The most important thing I learned is that AI is a powerful 
scaffold tool, but the human architect must make the final 
design decisions. Keeping responsibilities separated across 
classes made the system much easier to build, test, and extend.