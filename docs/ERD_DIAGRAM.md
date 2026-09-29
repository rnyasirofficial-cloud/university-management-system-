# University Management System (UMS) - Entity Relationship Diagram (ERD)

## SDAA Project Specification
- **Group Members:** Syed Ali Zaman, Muhammad Yasir Ali, Muhammad Umer
- **Total Entities:** 14 (Exceeds required minimum of 10)
- **Design:** Third Normal Form (3NF)

```mermaid
erDiagram
    DEPARTMENT ||--|{ PROGRAM : "offers"
    DEPARTMENT ||--|{ TEACHER : "employs"
    DEPARTMENT ||--|{ COURSE : "curates"
    
    PROGRAM ||--|{ STUDENT : "contains"
    
    COURSE ||--|{ COURSE_OFFERING : "instantiated_as"
    SEMESTER ||--|{ COURSE_OFFERING : "contains"
    TEACHER ||--|{ COURSE_OFFERING : "teaches"
    CLASSROOM ||--|{ COURSE_OFFERING : "assigned_to"
    
    STUDENT ||--|{ ENROLLMENT : "signs_up"
    COURSE_OFFERING ||--|{ ENROLLMENT : "includes"
    
    COURSE_OFFERING ||--|{ EXAM : "holds"
    STUDENT ||--|{ RESULT : "earns"
    EXAM ||--|{ RESULT : "evaluates"
    
    STUDENT ||--|{ ATTENDANCE : "logged_for"
    COURSE_OFFERING ||--|{ ATTENDANCE : "registers"
    
    COURSE_OFFERING ||--|{ TIMETABLE : "scheduled_in"
    CLASSROOM ||--|{ TIMETABLE : "booked_for"
    
    STUDENT ||--o| USER_ACCOUNT : "logs_in_as"
    TEACHER ||--o| USER_ACCOUNT : "logs_in_as"

    DEPARTMENT {
        int Department_ID PK
        string Department_Name UK
        string Department_Email UK
    }

    PROGRAM {
        int Program_ID PK
        string Program_Name
        string Degree_Level
        int Department_ID FK
    }

    STUDENT {
        int Student_ID PK
        string Registration_No UK
        string Student_Name
        string Email UK
        string Phone
        date Admission_Date
        int Program_ID FK
    }

    TEACHER {
        int Teacher_ID PK
        string Teacher_Name
        string Email UK
        string Phone
        string Designation
        int Department_ID FK
    }

    COURSE {
        int Course_ID PK
        string Course_Code UK
        string Course_Name
        int Credit_Hours
        int Department_ID FK
    }

    SEMESTER {
        int Semester_ID PK
        string Semester_Name
        int Year
        date Start_Date
        date End_Date
    }

    CLASSROOM {
        int Room_ID PK
        string Building_Name
        string Room_Number
        int Capacity
    }

    COURSE_OFFERING {
        int Offering_ID PK
        int Course_ID FK
        int Semester_ID FK
        int Teacher_ID FK
        int Room_ID FK
        string Section
    }

    ENROLLMENT {
        int Enrollment_ID PK
        int Student_ID FK
        int Offering_ID FK
        date Enrollment_Date
        string Status
    }

    EXAM {
        int Exam_ID PK
        int Offering_ID FK
        string Exam_Type
        date Exam_Date
        decimal Total_Marks
    }

    RESULT {
        int Result_ID PK
        int Student_ID FK
        int Exam_ID FK
        decimal Obtained_Marks
        string Grade
        decimal Grade_Point
    }

    ATTENDANCE {
        int Attendance_ID PK
        int Student_ID FK
        int Offering_ID FK
        date Attendance_Date
        string Status
    }

    TIMETABLE {
        int Timetable_ID PK
        int Offering_ID FK
        int Room_ID FK
        string Day
        time Start_Time
        time End_Time
    }

    USER_ACCOUNT {
        int User_ID PK
        string Username UK
        string Password
        string Role
        int Student_ID FK
        int Teacher_ID FK
    }
```
