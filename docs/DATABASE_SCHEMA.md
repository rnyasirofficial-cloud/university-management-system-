# University Management System (UMS) - Database Schema Specification

## SDAA Course Project
- **Project Title:** University Management System (UMS)
- **Group Members:**
  1. Syed Ali Zaman
  2. Muhammad Yasir Ali
  3. Muhammad Umer
- **Database Engine:** SQLite / MySQL / PostgreSQL Compatible
- **Design Standard:** Third Normal Form (3NF)

---

## 1. Normalization Breakdown to Third Normal Form (3NF)

### 1.1 First Normal Form (1NF)
A table is in 1NF if and only if:
1. Every attribute contains only atomic (indivisible) values.
2. There are no repeating groups or multi-valued attributes.
3. Each record is uniquely identified by a primary key.

**How our schema achieves 1NF:**
- In the `Student` and `Teacher` tables, phone numbers and emails are stored in distinct single-value columns without comma-separated strings or composite values.
- In `Course_Offering`, multiple students are not stored as arrays or lists; instead, individual registrations are stored in the discrete `Enrollment` table.

### 1.2 Second Normal Form (2NF)
A relation is in 2NF if:
1. It is in 1NF.
2. Every non-prime attribute is fully functionally dependent on the entire primary key (no partial dependencies on a composite candidate key).

**How our schema achieves 2NF:**
- In the `Enrollment` table, attributes such as `Course_Name` or `Student_Name` are **not** stored. Only `Enrollment_Date` and `Status` depend on the composite enrollment relationship.
- In `Result`, exam metadata (such as `Total_Marks` or `Exam_Date`) is stored strictly in `Exam`, so `Result` only holds `Obtained_Marks`, `Grade`, and `Grade_Point` which depend on the specific student-exam pair.

### 1.3 Third Normal Form (3NF)
A relation is in 3NF if:
1. It is in 2NF.
2. There are no transitive dependencies: non-prime attributes do not depend on other non-prime attributes ($X \rightarrow Y$ where $Y$ is not a subset of any candidate key and $X$ is not a superkey).

**How our schema achieves 3NF:**
- Department names are **not** replicated in the `Student`, `Teacher`, or `Course` tables.
- Instead, each of those entities references `Department_ID` as a Foreign Key.
- Similarly, a student's degree program is referenced via `Program_ID`, rather than storing program names or department names in `Student`.
- Transitive chains such as $\text{Student} \rightarrow \text{Program} \rightarrow \text{Department}$ are strictly separated across normalized tables.

---

## 2. Comprehensive Data Dictionary (14 Entities)

| Table # | Entity Name | Primary Key | Foreign Keys | Key Attributes & Constraints |
|---|---|---|---|---|
| **1** | `Department` | `Department_ID` | None | `Department_Name` (Unique), `Department_Email` (Unique) |
| **2** | `Program` | `Program_ID` | `Department_ID` $\rightarrow$ `Department` | `Program_Name`, `Degree_Level` |
| **3** | `Student` | `Student_ID` | `Program_ID` $\rightarrow$ `Program` | `Registration_No` (Unique), `Student_Name`, `Email`, `Phone`, `Admission_Date` |
| **4** | `Teacher` | `Teacher_ID` | `Department_ID` $\rightarrow$ `Department` | `Teacher_Name`, `Email` (Unique), `Phone`, `Designation` |
| **5** | `Course` | `Course_ID` | `Department_ID` $\rightarrow$ `Department` | `Course_Code` (Unique), `Course_Name`, `Credit_Hours` (1-6) |
| **6** | `Semester` | `Semester_ID` | None | `Semester_Name`, `Year`, `Start_Date`, `End_Date`, Unique(`Semester_Name`, `Year`) |
| **7** | `Classroom` | `Room_ID` | None | `Building_Name`, `Room_Number`, `Capacity` (> 0), Unique(`Building`, `Room`) |
| **8** | `Course_Offering`| `Offering_ID` | `Course_ID`, `Semester_ID`, `Teacher_ID`, `Room_ID` | `Section`, Unique(`Course_ID`, `Semester_ID`, `Section`) |
| **9** | `Enrollment` | `Enrollment_ID` | `Student_ID` $\rightarrow$ `Student`, `Offering_ID` $\rightarrow$ `Course_Offering` | `Enrollment_Date`, `Status` (Enrolled/Dropped/Completed), Unique(`Student`, `Offering`) |
| **10** | `Exam` | `Exam_ID` | `Offering_ID` $\rightarrow$ `Course_Offering` | `Exam_Type` (Midterm/Final/Quiz), `Exam_Date`, `Total_Marks` |
| **11** | `Result` | `Result_ID` | `Student_ID` $\rightarrow$ `Student`, `Exam_ID` $\rightarrow$ `Exam` | `Obtained_Marks`, `Grade`, `Grade_Point`, Unique(`Student`, `Exam`) |
| **12** | `Attendance` | `Attendance_ID` | `Student_ID` $\rightarrow$ `Student`, `Offering_ID` $\rightarrow$ `Course_Offering` | `Attendance_Date`, `Status` (Present/Absent/Late), Unique(`Student`, `Offering`, `Date`) |
| **13** | `Timetable` | `Timetable_ID` | `Offering_ID` $\rightarrow$ `Offering`, `Room_ID` $\rightarrow$ `Classroom` | `Day`, `Start_Time`, `End_Time` |
| **14** | `User_Account` | `User_ID` | `Student_ID` (opt), `Teacher_ID` (opt) | `Username` (Unique), `Password` (Hashed), `Role` (Admin/Teacher/Student) |

---

## 3. Referential Integrity Rules
- **Department $\rightarrow$ Program / Teacher / Course:** `ON DELETE RESTRICT` (Protects academic structure from accidental cascading deletions).
- **Course_Offering $\rightarrow$ Enrollment / Exam / Timetable / Attendance:** `ON DELETE CASCADE` (Removing a course section safely purges its dependent schedules and exams).
- **User_Account $\rightarrow$ Student / Teacher:** `ON DELETE SET NULL` (Deleting a profile does not corrupt security user logs).
