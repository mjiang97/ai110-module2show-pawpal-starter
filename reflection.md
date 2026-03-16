# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Core user actions:
1. Add a pet: A user can register a new pet with its name, species, age, 
   and specific care needs.
2. Schedule a task: A user can create care tasks (e.g., walk, feeding, 
   vet appointment) assigned to a specific pet at a scheduled time.
3. View today's tasks: A user can see all tasks scheduled for the current 
   day, sorted by time or priority.
- What classes did you include, and what responsibilities did you assign to each?
- **Owner**: Represents the user of the app. Holds a name and a list of 
  pets. Responsible for adding/removing pets.

- **Pet**: Represents an individual pet. Stores name, species, age, and 
  care needs. Each Pet belongs to one Owner and can have multiple Tasks 
  associated with it.

- **Task**: Represents a single care activity (walk, feeding, vet visit). 
  Stores a description, scheduled date/time, priority level, and status 
  (pending/completed). Each Task is linked to one Pet.

- **Scheduler**: Manages the collection of all Tasks. Responsible for 
  adding new tasks, retrieving tasks by date (e.g., today's tasks), and 
  sorting them by time or priority.

**b. Design changes**

- Did your design change during implementation?

Yes. The biggest change was removing `tasks` from `Pet` entirely. The original UML stored tasks in both `Pet.tasks` and `Scheduler.tasks`, which meant the two lists could easily go out of sync. We made `Scheduler` the single source of truth and had `Pet` delegate all task operations to it through a `_scheduler` reference set by `Owner`. We also added `Owner.scheduler`, cascade deletion in `remove_pet`, and input validation on `Task` via `__post_init__` — none of which were in the original UML.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
