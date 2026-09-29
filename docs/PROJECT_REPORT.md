# UNIVERSITY MANAGEMENT SYSTEM (UMS)
## Comprehensive SDAA Project Implementation Report & Academic Documentation

### Group Information
- **Course:** System Design & Architecture / Analysis (SDAA)
- **Project Title:** University Management System (UMS)
- **Group Members:**
  1. **Syed Ali Zaman**
  2. **Muhammad Yasir Ali**
  3. **Muhammad Umer**
- **Architecture Standard:** Object-Oriented Domain Architecture (OOP) & 3NF Relational Database
- **Date:** Academic Term 2026-2027

---

## 1. Executive Summary & Objectives

The University Management System (UMS) provides a centralized, relational software system designed to eliminate manual data entry discrepancies, duplicate entries, and operational delays in university academic administration.

### Key Project Objectives Achieved:
1. **Full Academic Lifecycle Management:** Seamless handling of departments, academic degree programs, courses, classrooms, faculty, students, semesters, and course offerings.
2. **Third Normal Form (3NF) Relational Database:** All 14 entities are normalized to 3NF, guaranteeing atomic attributes (1NF), zero partial dependencies (2NF), and zero transitive functional dependencies (3NF).
3. **Object-Oriented Domain Classes (OOP):** Implementation of object models with encapsulation, validation methods, GPA computation algorithms, attendance percentage calculations, and timetable conflict detection.
4. **Interactive Enterprise Web Application:** Built with Python (FastAPI), modern CSS design tokens, dynamic JavaScript SPA architecture, dark/light theme switching, and live database schema verification.
5. **Role-Based Access Control:** Configured for Administrator, Teacher, and Student user roles.

---

## 2. System Architecture & 14 Domain Entities (3NF)

The system fulfills and exceeds the project proposal requirement of 10+ entities by providing **14 normalized entities**:

1. **`Department`** (`Department_ID`, `Department_Name`, `Department_Email`)
2. **`Program`** (`Program_ID`, `Program_Name`, `Degree_Level`, `Department_ID`)
3. **`Student`** (`Student_ID`, `Registration_No`, `Student_Name`, `Email`, `Phone`, `Admission_Date`, `Program_ID`)
4. **`Teacher`** (`Teacher_ID`, `Teacher_Name`, `Email`, `Phone`, `Designation`, `Department_ID`)
5. **`Course`** (`Course_ID`, `Course_Code`, `Course_Name`, `Credit_Hours`, `Department_ID`, `Course_Description`)
6. **`Semester`** (`Semester_ID`, `Semester_Name`, `Year`, `Start_Date`, `End_Date`)
7. **`Classroom`** (`Room_ID`, `Building_Name`, `Room_Number`, `Capacity`)
8. **`Course_Offering`** (`Offering_ID`, `Course_ID`, `Semester_ID`, `Teacher_ID`, `Room_ID`, `Section`)
9. **`Enrollment`** (`Enrollment_ID`, `Student_ID`, `Offering_ID`, `Enrollment_Date`, `Status`)
10. **`Exam`** (`Exam_ID`, `Offering_ID`, `Exam_Type`, `Exam_Date`, `Total_Marks`)
11. **`Result`** (`Result_ID`, `Student_ID`, `Exam_ID`, `Obtained_Marks`, `Grade`, `Grade_Point`)
12. **`Attendance`** (`Attendance_ID`, `Student_ID`, `Offering_ID`, `Attendance_Date`, `Status`)
13. **`Timetable`** (`Timetable_ID`, `Offering_ID`, `Room_ID`, `Day`, `Start_Time`, `End_Time`)
14. **`User_Account`** (`User_ID`, `Username`, `Password`, `Role`, `Student_ID`, `Teacher_ID`)

---

## 3. Object-Oriented Domain Classes & Methods

All classes reside in the `classes/` module and extend `BaseEntity`:

### 3.1 `Student` Class
- **Attributes:** `student_id`, `registration_no`, `student_name`, `email`, `phone`, `admission_date`, `program_id`
- **Method `calculate_gpa(results)`:** Computes Quality Points divided by Total Credits to yield standard CGPA.
- **Method `calculate_attendance_percentage(attendance_records)`:** Determines physical attendance rate.

### 3.2 `Result` Class
- **Method `compute_grade(obtained, total)`:** Automatically computes letter grade (`A+`, `A`, `B+`, `B`, `C+`, `C`, `D`, `F`) and 4.0 scale Grade Points.

### 3.3 `Timetable` Class
- **Method `conflicts_with(other)`:** Prevents classroom double-booking during overlapping hours on the same weekday.

### 3.4 `UserAccount` Class
- **Method `hash_password(raw)`:** Encrypts user credentials with cryptographic SHA-256 hashing.
- **Method `verify_password(raw)`:** Verifies user identity during authentication.

---

---

## 4. Official Class Timetable & Faculty Dataset (GCUF Software Engineering)

The live database is pre-configured with the official **GCUF Department of Software Engineering (BS(SE) 5th Eve-B, Fall 2026)** timetable:

| Day | Time | Course Code & Title | Type | Instructor | Classroom / Lab |
|---|---|---|---|---|---|
| **Monday** | 14:00 - 15:00 | HCI & CG (Human Computer Interaction) | Lecture | Mr. Syed Sajjad | Sports Blk |
| **Monday** | 15:00 - 16:00 | Info. Sec (Information Security) | Lecture | Mr. Nauman | Sports Blk |
| **Monday** | 16:00 - 18:00 | Info. Sec (Information Security Lab) | Lab | Mr. Nauman | SE Lab-2 |
| **Monday** | 18:00 - 19:00 | AI (Artificial Intelligence) | Lecture | Mr. Syed Sajjad | Sports Blk |
| **Tuesday** | 15:00 - 16:00 | SDaA (Software Design & Architecture) | Lecture | Dr. Khurram | RLab |
| **Tuesday** | 16:00 - 18:00 | SDaA (Software Design & Architecture Lab) | Lab | Dr. Khurram | RLab |
| **Tuesday** | 18:00 - 19:00 | CO&AL (Computer Org & Assembly Lang) | Lecture | Dr. Qamar | Room-1 |
| **Wednesday** | 13:00 - 14:00 | SDaA (Software Design & Architecture) | Lecture | Dr. Khurram | Room-3 |
| **Wednesday** | 14:00 - 15:00 | THQ III (Translation of Holy Quran III) | Lecture | Mr. Talib | Room-2 |
| **Wednesday** | 15:00 - 16:00 | CO&AL (Computer Org & Assembly Lang) | Lecture | Dr. Qamar | Room-1 |
| **Wednesday** | 16:00 - 18:00 | CO&AL (Computer Org & Assembly Lab) | Lab | Dr. Qamar | Room-1 |
| **Thursday** | 13:00 - 14:00 | Web Eng (Web Engineering) | Lecture | Mr. Noman S | SE Hall 2 |
| **Thursday** | 14:00 - 16:00 | Web Eng (Web Engineering Lab) | Lab | Mr. Noman S | Sports Blk |
| **Thursday** | 16:00 - 17:00 | Info. Sec (Information Security) | Lecture | Mr. Nauman | Sports Blk |
| **Thursday** | 17:00 - 19:00 | AI (Artificial Intelligence Lab) | Lab | Mr. Syed Sajjad | SE Lab-2 |
| **Friday** | 14:00 - 15:00 | Web Eng (Web Engineering) | Lecture | Mr. Noman S | Room-3 |
| **Friday** | 15:00 - 16:00 | AI (Artificial Intelligence) | Lecture | Mr. Syed Sajjad | Sports Blk |
| **Friday** | 16:00 - 17:00 | HCI & CG (Human Computer Interaction) | Lecture | Mr. Syed Sajjad | Sports Blk |
| **Friday** | 17:00 - 19:00 | HCI & CG (HCI & CG Lab) | Lab | Mr. Syed Sajjad | Sports Blk |

---

## 5. How to Run and Demonstrate to Lecturer

1. Open folder in terminal or double-click `run.bat`.
2. Start server command:
   ```bash
   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```
3. Open browser at: `http://127.0.0.1:8000`
4. Use the top navigation or role switcher to demonstrate:
   - **Official Timetable:** Click "Weekly Timetable" to showcase the complete visual schedule grid organized by day, highlighting labs and lecture halls.
   - **Faculty Records:** Click "Faculty & Teachers" to view Dr. Khurram, Dr. Qamar, Mr. Syed Sajjad, Mr. Nauman, Mr. Noman S, and Mr. Talib.
   - **Student Transcript & CGPA:** Click "Students" $\rightarrow$ "🎓 Transcript & GPA" to view Syed Ali Zaman's official transcript and CGPA calculation across 5th semester courses.
   - **3NF Schema Inspector:** Click "3NF Schema Inspector" to show live table structures and foreign key references.
   - **Reset Sample DB:** Instant one-click reset button for demonstrations.
