# University Management System (UMS)
> **SDAA Project Proposal Implementation (3NF Relational Database & OOP Architecture)**

### Group Members:
1. **Syed Ali Zaman**
2. **Muhammad Yasir Ali**
3. **Muhammad Umer**

---

## 🌟 Highlights
- **14 Relational 3NF Entities** (Exceeds required minimum of 10)
- **Official GCUF Timetable & Faculty Pre-loaded:** Full 19-slot Monday-Friday schedule for **BS(SE) 5th Eve-B** with Dr. Khurram (SDaA), Dr. Qamar (CO&AL), Mr. Syed Sajjad (AI, HCI & CG), Mr. Nauman (Info. Sec), Mr. Noman S (Web Eng), and Mr. Talib (THQ III).
- **Dedicated Student Portal (`view-student-portal`):** Displays student registration details, 7 active semester courses, today's lecture schedule, verified attendance (100%), and calculated CGPA (4.00) with official transcript printing.
- **Interactive 3NF SQL Query Runner:** Execute custom SQL queries with multi-table joins or one-click preset queries right from the web browser.
- **Object-Oriented Domain Architecture (`classes/`):** Clean domain models with business methods (GPA calculation, grade point computing, timetable conflict detection, attendance percentages).
- **Interactive Web Dashboard:** Dark/light mode switcher, role-based demonstration mode (Admin, Teacher Dr. Khurram, Student Syed Ali Zaman), and 1-click database reset.
- **Full Academic Documentation:**
  - [DATABASE_SCHEMA.md](file:///docs/DATABASE_SCHEMA.md) (1NF, 2NF, 3NF proofs & data dictionary)
  - [CLASS_DIAGRAM.md](file:///docs/CLASS_DIAGRAM.md) (Mermaid UML Class Diagram)
  - [ERD_DIAGRAM.md](file:///docs/ERD_DIAGRAM.md) (Mermaid Entity Relationship Diagram)
  - [PROJECT_REPORT.md](file:///docs/PROJECT_REPORT.md) (Academic presentation report)

---

## 🚀 Quick Start Instructions

### Option 1: Double Click `run.bat`
Simply double-click the `run.bat` file in Windows Explorer. It will start the server and open your browser automatically.

### Option 2: Command Line
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
Then navigate to: **`http://127.0.0.1:8000`**

---

## 📂 Project Structure
```
University Management System/
│
├── database/
│   ├── schema.sql           # 3NF SQLite/PostgreSQL/MySQL compliant schema (all 14 tables)
│   ├── seed.sql             # Comprehensive seed data for all entities
│   ├── db.py                # Database helper & connection manager
│   └── university.db        # SQLite database file
│
├── classes/                 # OOP Domain Entities with Business Logic
│   ├── base.py              # BaseEntity class
│   ├── department_program.py# Department & Program classes
│   ├── student_teacher.py   # Student (with GPA calc) & Teacher classes
│   ├── academic.py          # Course, Semester, Classroom, CourseOffering, Enrollment
│   ├── examination.py       # Exam, Result (with grade computing), Attendance, Timetable, UserAccount
│   └── __init__.py          # Clean module exports
│
├── docs/                    # Complete Academic Documentation
│   ├── DATABASE_SCHEMA.md   # 3NF normalization analysis and data dictionary
│   ├── CLASS_DIAGRAM.md     # UML Class diagram with Mermaid
│   ├── ERD_DIAGRAM.md       # Entity-Relationship diagram
│   └── PROJECT_REPORT.md    # Formal submission report
│
├── static/                  # Modern Web Dashboard
│   ├── css/style.css        # Responsive dark/light theme stylesheet
│   ├── js/app.js            # Single Page Application frontend logic
│   └── index.html           # Main user interface
│
├── app.py                   # FastAPI REST backend & static server
├── run.bat                  # One-click Windows launch script
└── README.md                # Documentation & instructions
```
