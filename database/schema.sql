-- ============================================================================
-- UNIVERSITY MANAGEMENT SYSTEM (UMS)
-- System Design & Architecture Analysis (SDAA) Project
-- Group Members: Syed Ali Zaman, Muhammad Yasir Ali, Muhammad Umer
-- Relational Database Schema in Third Normal Form (3NF)
-- Compatible with SQLite, MySQL, and PostgreSQL
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. DEPARTMENT ENTITY
-- Stores academic departments within the university
CREATE TABLE IF NOT EXISTS Department (
    Department_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Department_Name VARCHAR(100) NOT NULL UNIQUE,
    Department_Email VARCHAR(100) NOT NULL UNIQUE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. PROGRAM ENTITY
-- Academic degree programs offered by departments
CREATE TABLE IF NOT EXISTS Program (
    Program_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Program_Name VARCHAR(100) NOT NULL,
    Degree_Level VARCHAR(50) NOT NULL, -- e.g., 'Undergraduate (BS)', 'Graduate (MS)', 'Postgraduate (PhD)'
    Department_ID INTEGER NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 3. STUDENT ENTITY
-- Records of registered students in programs
CREATE TABLE IF NOT EXISTS Student (
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Registration_No VARCHAR(50) NOT NULL UNIQUE,
    Student_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(25) NOT NULL,
    Admission_Date DATE NOT NULL,
    Program_ID INTEGER NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Program_ID) REFERENCES Program(Program_ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 4. TEACHER ENTITY
-- Academic faculty members and their departments
CREATE TABLE IF NOT EXISTS Teacher (
    Teacher_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Teacher_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(25) NOT NULL,
    Designation VARCHAR(50) NOT NULL, -- e.g., 'Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer'
    Department_ID INTEGER NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 5. COURSE ENTITY
-- Master list of academic courses
CREATE TABLE IF NOT EXISTS Course (
    Course_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Course_Code VARCHAR(20) NOT NULL UNIQUE,
    Course_Name VARCHAR(100) NOT NULL,
    Credit_Hours INTEGER NOT NULL CHECK (Credit_Hours BETWEEN 1 AND 6),
    Department_ID INTEGER NOT NULL,
    Course_Description TEXT,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 6. SEMESTER ENTITY
-- Academic terms/sessions
CREATE TABLE IF NOT EXISTS Semester (
    Semester_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Semester_Name VARCHAR(50) NOT NULL, -- e.g., 'Fall', 'Spring', 'Summer'
    Year INTEGER NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT UQ_Semester UNIQUE (Semester_Name, Year)
);

-- 7. CLASSROOM ENTITY
-- Physical campus rooms and lab facilities
CREATE TABLE IF NOT EXISTS Classroom (
    Room_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Building_Name VARCHAR(50) NOT NULL,
    Room_Number VARCHAR(20) NOT NULL,
    Capacity INTEGER NOT NULL CHECK (Capacity > 0),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT UQ_Classroom UNIQUE (Building_Name, Room_Number)
);

-- 8. COURSE_OFFERING ENTITY
-- Specific course instances scheduled for a semester with an assigned instructor and primary room
CREATE TABLE IF NOT EXISTS Course_Offering (
    Offering_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Course_ID INTEGER NOT NULL,
    Semester_ID INTEGER NOT NULL,
    Teacher_ID INTEGER NOT NULL,
    Room_ID INTEGER NOT NULL,
    Section VARCHAR(10) DEFAULT 'A',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Semester_ID) REFERENCES Semester(Semester_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Teacher_ID) REFERENCES Teacher(Teacher_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Room_ID) REFERENCES Classroom(Room_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT UQ_Offering UNIQUE (Course_ID, Semester_ID, Section)
);

-- 9. ENROLLMENT ENTITY (Resolves Many-to-Many between Student and Course_Offering)
-- Tracks registered courses for each student
CREATE TABLE IF NOT EXISTS Enrollment (
    Enrollment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Offering_ID INTEGER NOT NULL,
    Enrollment_Date DATE NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Enrolled' CHECK (Status IN ('Enrolled', 'Dropped', 'Completed', 'Withdrawn')),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Offering_ID) REFERENCES Course_Offering(Offering_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT UQ_Enrollment UNIQUE (Student_ID, Offering_ID)
);

-- 10. EXAM ENTITY
-- Scheduled assessments and exams for course offerings
CREATE TABLE IF NOT EXISTS Exam (
    Exam_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Offering_ID INTEGER NOT NULL,
    Exam_Type VARCHAR(30) NOT NULL CHECK (Exam_Type IN ('Midterm', 'Final', 'Quiz', 'Assignment', 'Project')),
    Exam_Date DATE NOT NULL,
    Total_Marks DECIMAL(5, 2) NOT NULL CHECK (Total_Marks > 0),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Offering_ID) REFERENCES Course_Offering(Offering_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 11. RESULT ENTITY
-- Student scores, computed grades and grade points for an exam
CREATE TABLE IF NOT EXISTS Result (
    Result_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Exam_ID INTEGER NOT NULL,
    Obtained_Marks DECIMAL(5, 2) NOT NULL CHECK (Obtained_Marks >= 0),
    Grade VARCHAR(5) NOT NULL,
    Grade_Point DECIMAL(3, 2) NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Exam_ID) REFERENCES Exam(Exam_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT UQ_Student_Exam UNIQUE (Student_ID, Exam_ID)
);

-- 12. ATTENDANCE ENTITY
-- Attendance tracking per lecture session per enrolled student
CREATE TABLE IF NOT EXISTS Attendance (
    Attendance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Offering_ID INTEGER NOT NULL,
    Attendance_Date DATE NOT NULL,
    Status VARCHAR(20) NOT NULL CHECK (Status IN ('Present', 'Absent', 'Late', 'Excused')),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Offering_ID) REFERENCES Course_Offering(Offering_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT UQ_Student_Offering_Date UNIQUE (Student_ID, Offering_ID, Attendance_Date)
);

-- 13. TIMETABLE ENTITY
-- Weekly schedule of class sessions across classrooms and time slots
CREATE TABLE IF NOT EXISTS Timetable (
    Timetable_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Offering_ID INTEGER NOT NULL,
    Room_ID INTEGER NOT NULL,
    Day VARCHAR(20) NOT NULL CHECK (Day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Offering_ID) REFERENCES Course_Offering(Offering_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Room_ID) REFERENCES Classroom(Room_ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 14. USER_ACCOUNT ENTITY
-- Authentication and role-based authorization for Admin, Teacher, and Student
CREATE TABLE IF NOT EXISTS User_Account (
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL, -- SHA-256 / bcrypt hash
    Role VARCHAR(20) NOT NULL CHECK (Role IN ('Administrator', 'Teacher', 'Student')),
    Student_ID INTEGER NULL,
    Teacher_ID INTEGER NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (Teacher_ID) REFERENCES Teacher(Teacher_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- INDEXES FOR QUERY OPTIMIZATION & PERFORMANCE (SDAA High Performance Requirements)
CREATE INDEX IF NOT EXISTS idx_student_program ON Student(Program_ID);
CREATE INDEX IF NOT EXISTS idx_program_dept ON Program(Department_ID);
CREATE INDEX IF NOT EXISTS idx_teacher_dept ON Teacher(Department_ID);
CREATE INDEX IF NOT EXISTS idx_course_dept ON Course(Department_ID);
CREATE INDEX IF NOT EXISTS idx_offering_course ON Course_Offering(Course_ID);
CREATE INDEX IF NOT EXISTS idx_offering_semester ON Course_Offering(Semester_ID);
CREATE INDEX IF NOT EXISTS idx_offering_teacher ON Course_Offering(Teacher_ID);
CREATE INDEX IF NOT EXISTS idx_enrollment_student ON Enrollment(Student_ID);
CREATE INDEX IF NOT EXISTS idx_enrollment_offering ON Enrollment(Offering_ID);
CREATE INDEX IF NOT EXISTS idx_exam_offering ON Exam(Offering_ID);
CREATE INDEX IF NOT EXISTS idx_result_student ON Result(Student_ID);
CREATE INDEX IF NOT EXISTS idx_result_exam ON Result(Exam_ID);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON Attendance(Student_ID);
CREATE INDEX IF NOT EXISTS idx_attendance_offering ON Attendance(Offering_ID);
CREATE INDEX IF NOT EXISTS idx_timetable_offering ON Timetable(Offering_ID);
CREATE INDEX IF NOT EXISTS idx_timetable_room ON Timetable(Room_ID);
