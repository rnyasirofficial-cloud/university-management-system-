"""
University Management System (UMS) - FastAPI Server
Provides RESTful APIs for all 14 3NF Entities, Authentication, OOP Business Logic,
and serves the modern Web Application interface.
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from pathlib import Path
import hashlib

from database.db import get_connection, init_database, query_all, query_one, execute_commit
from classes import (
    Department, Program, Student, Teacher, Course,
    Semester, Classroom, CourseOffering, Enrollment,
    Exam, Result, Attendance, Timetable, UserAccount
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="University Management System API",
    description="SDAA Project API with 14 3NF Entities and OOP Domain Architecture",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure database is initialized on startup
@app.on_event("startup")
def startup_event():
    init_database(force_reseed=False)

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


# ============================================================================
# PYDANTIC SCHEMAS FOR API INPUTS
# ============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str

class DepartmentCreate(BaseModel):
    department_name: str
    department_email: str

class ProgramCreate(BaseModel):
    program_name: str
    degree_level: str
    department_id: int

class StudentCreate(BaseModel):
    registration_no: str
    student_name: str
    email: str
    phone: str
    admission_date: str
    program_id: int

class TeacherCreate(BaseModel):
    teacher_name: str
    email: str
    phone: str
    designation: str
    department_id: int

class CourseCreate(BaseModel):
    course_code: str
    course_name: str
    credit_hours: int
    department_id: int
    course_description: Optional[str] = ""

class SemesterCreate(BaseModel):
    semester_name: str
    year: int
    start_date: str
    end_date: str

class ClassroomCreate(BaseModel):
    building_name: str
    room_number: str
    capacity: int

class OfferingCreate(BaseModel):
    course_id: int
    semester_id: int
    teacher_id: int
    room_id: int
    section: Optional[str] = "A"

class EnrollmentCreate(BaseModel):
    student_id: int
    offering_id: int
    enrollment_date: str
    status: Optional[str] = "Enrolled"

class ExamCreate(BaseModel):
    offering_id: int
    exam_type: str
    exam_date: str
    total_marks: float

class ResultCreate(BaseModel):
    student_id: int
    exam_id: int
    obtained_marks: float

class AttendanceCreate(BaseModel):
    student_id: int
    offering_id: int
    attendance_date: str
    status: str

class TimetableCreate(BaseModel):
    offering_id: int
    room_id: int
    day: str
    start_time: str
    end_time: str

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    department_email: Optional[str] = None

class ProgramUpdate(BaseModel):
    program_name: Optional[str] = None
    degree_level: Optional[str] = None
    department_id: Optional[int] = None

class StudentUpdate(BaseModel):
    registration_no: Optional[str] = None
    student_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    admission_date: Optional[str] = None
    program_id: Optional[int] = None

class TeacherUpdate(BaseModel):
    teacher_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    designation: Optional[str] = None
    department_id: Optional[int] = None

class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    credit_hours: Optional[int] = None
    department_id: Optional[int] = None
    course_description: Optional[str] = None

class SemesterUpdate(BaseModel):
    semester_name: Optional[str] = None
    year: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ClassroomUpdate(BaseModel):
    building_name: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None

class OfferingUpdate(BaseModel):
    course_id: Optional[int] = None
    semester_id: Optional[int] = None
    teacher_id: Optional[int] = None
    room_id: Optional[int] = None
    section: Optional[str] = None

class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    offering_id: Optional[int] = None
    enrollment_date: Optional[str] = None
    status: Optional[str] = None

class ExamUpdate(BaseModel):
    offering_id: Optional[int] = None
    exam_type: Optional[str] = None
    exam_date: Optional[str] = None
    total_marks: Optional[float] = None

class ResultUpdate(BaseModel):
    student_id: Optional[int] = None
    exam_id: Optional[int] = None
    obtained_marks: Optional[float] = None

class AttendanceUpdate(BaseModel):
    student_id: Optional[int] = None
    offering_id: Optional[int] = None
    attendance_date: Optional[str] = None
    status: Optional[str] = None

class TimetableUpdate(BaseModel):
    offering_id: Optional[int] = None
    room_id: Optional[int] = None
    day: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None


# ============================================================================
# AUTHENTICATION & SESSION
# ============================================================================

@app.post("/api/login")
def login(creds: LoginRequest):
    pwd_hash = hashlib.sha256(creds.password.encode("utf-8")).hexdigest()
    user = query_one(
        """
        SELECT u.User_ID, u.Username, u.Role, u.Student_ID, u.Teacher_ID,
               s.Student_Name, t.Teacher_Name
        FROM User_Account u
        LEFT JOIN Student s ON u.Student_ID = s.Student_ID
        LEFT JOIN Teacher t ON u.Teacher_ID = t.Teacher_ID
        WHERE u.Username = ? AND u.Password = ?
        """,
        (creds.username, pwd_hash)
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    display_name = user.get("Student_Name") or user.get("Teacher_Name") or user["Username"]
    return {
        "success": True,
        "user_id": user["User_ID"],
        "username": user["Username"],
        "role": user["Role"],
        "student_id": user["Student_ID"],
        "teacher_id": user["Teacher_ID"],
        "display_name": display_name
    }


# ============================================================================
# SYSTEM OVERVIEW & METRICS
# ============================================================================

@app.get("/api/stats")
def get_system_stats():
    total_students = query_one("SELECT COUNT(*) AS c FROM Student")["c"]
    total_teachers = query_one("SELECT COUNT(*) AS c FROM Teacher")["c"]
    total_courses = query_one("SELECT COUNT(*) AS c FROM Course")["c"]
    total_offerings = query_one("SELECT COUNT(*) AS c FROM Course_Offering")["c"]
    total_departments = query_one("SELECT COUNT(*) AS c FROM Department")["c"]
    total_programs = query_one("SELECT COUNT(*) AS c FROM Program")["c"]
    total_enrollments = query_one("SELECT COUNT(*) AS c FROM Enrollment")["c"]
    
    # Calculate average grade point across all results
    avg_gp = query_one("SELECT AVG(Grade_Point) AS avg_gp FROM Result")["avg_gp"] or 0.0

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "total_offerings": total_offerings,
        "total_departments": total_departments,
        "total_programs": total_programs,
        "total_enrollments": total_enrollments,
        "average_gpa": round(avg_gp, 2)
    }


@app.get("/api/schema-info")
def get_schema_info():
    """Returns metadata for all 14 entities and their row counts for lecturer inspection."""
    tables = [
        "Department", "Program", "Student", "Teacher", "Course",
        "Semester", "Classroom", "Course_Offering", "Enrollment",
        "Exam", "Result", "Attendance", "Timetable", "User_Account"
    ]
    info = []
    for tbl in tables:
        count = query_one(f"SELECT COUNT(*) AS c FROM {tbl}")["c"]
        cols = query_all(f"PRAGMA table_info({tbl});")
        fks = query_all(f"PRAGMA foreign_key_list({tbl});")
        info.append({
            "table_name": tbl,
            "row_count": count,
            "columns": cols,
            "foreign_keys": fks
        })
    return info


class SqlQueryRequest(BaseModel):
    query: str

@app.post("/api/execute-sql")
def execute_custom_sql(req: SqlQueryRequest):
    """Executes CRUD-capable SQL queries for the interactive schema runner."""
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="SQL query cannot be empty.")

    if q.count(";") > 1:
        raise HTTPException(status_code=400, detail="Only a single SQL statement is allowed in the runner.")

    clean_q = q.lstrip(";\n\r\t ")
    normalized = clean_q.upper()
    allowed_prefixes = ("SELECT", "PRAGMA", "EXPLAIN", "INSERT", "UPDATE", "DELETE")
    if not normalized.startswith(allowed_prefixes):
        raise HTTPException(status_code=400, detail="Only SELECT, INSERT, UPDATE, DELETE, PRAGMA, and EXPLAIN statements are allowed in the SQL runner.")
    if "DROP " in normalized or "ALTER " in normalized or "CREATE " in normalized or "TRUNCATE " in normalized:
        raise HTTPException(status_code=400, detail="DDL statements are disabled in the SQL runner for safety.")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(clean_q)
        if clean_q.upper().startswith(("SELECT", "PRAGMA", "EXPLAIN")):
            rows = cursor.fetchall()
            columns = list(rows[0].keys()) if rows else []
            conn.close()
            return {
                "success": True,
                "count": len(rows),
                "columns": columns,
                "rows": [dict(row) for row in rows]
            }
        conn.commit()
        result = {
            "success": True,
            "count": cursor.rowcount,
            "lastrowid": cursor.lastrowid,
            "rows": [],
            "columns": []
        }
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/reset-db")
def reset_database():
    """Resets the database with pristine seed data."""
    init_database(force_reseed=True)
    return {"message": "Database reset and seeded successfully!"}


# ============================================================================
# MODULE 1: DEPARTMENTS
# ============================================================================

@app.get("/api/departments")
def list_departments():
    return query_all("SELECT * FROM Department ORDER BY Department_ID ASC")

@app.post("/api/departments")
def create_department(dept: DepartmentCreate):
    model = Department(dept.department_name, dept.department_email)
    model.validate()
    try:
        new_id = execute_commit(
            "INSERT INTO Department (Department_Name, Department_Email) VALUES (?, ?)",
            (model.department_name, model.department_email)
        )
        return {"department_id": new_id, "message": "Department created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/departments/{department_id}")
def get_department(department_id: int):
    item = query_one("SELECT * FROM Department WHERE Department_ID = ?", (department_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    return item

@app.put("/api/departments/{department_id}")
def update_department(department_id: int, dept: DepartmentUpdate):
    existing = query_one("SELECT * FROM Department WHERE Department_ID = ?", (department_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Department not found")

    payload = {
        "department_name": dept.department_name or existing["Department_Name"],
        "department_email": dept.department_email or existing["Department_Email"]
    }
    model = Department(payload["department_name"], payload["department_email"])
    model.validate()

    execute_commit(
        "UPDATE Department SET Department_Name = ?, Department_Email = ? WHERE Department_ID = ?",
        (model.department_name, model.department_email, department_id)
    )
    return {"department_id": department_id, "message": "Department updated successfully"}

@app.delete("/api/departments/{department_id}")
def delete_department(department_id: int):
    if not query_one("SELECT 1 FROM Department WHERE Department_ID = ?", (department_id,)):
        raise HTTPException(status_code=404, detail="Department not found")
    try:
        execute_commit("DELETE FROM Department WHERE Department_ID = ?", (department_id,))
        return {"department_id": department_id, "message": "Department deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 2: PROGRAMS
# ============================================================================

@app.get("/api/programs")
def list_programs():
    return query_all("""
        SELECT p.*, d.Department_Name
        FROM Program p
        JOIN Department d ON p.Department_ID = d.Department_ID
        ORDER BY p.Program_ID ASC
    """)

@app.post("/api/programs")
def create_program(prog: ProgramCreate):
    model = Program(prog.program_name, prog.degree_level, prog.department_id)
    model.validate()
    try:
        new_id = execute_commit(
            "INSERT INTO Program (Program_Name, Degree_Level, Department_ID) VALUES (?, ?, ?)",
            (model.program_name, model.degree_level, model.department_id)
        )
        return {"program_id": new_id, "message": "Program created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/programs/{program_id}")
def get_program(program_id: int):
    item = query_one("""
        SELECT p.*, d.Department_Name
        FROM Program p
        JOIN Department d ON p.Department_ID = d.Department_ID
        WHERE p.Program_ID = ?
    """, (program_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Program not found")
    return item

@app.put("/api/programs/{program_id}")
def update_program(program_id: int, prog: ProgramUpdate):
    existing = query_one("SELECT * FROM Program WHERE Program_ID = ?", (program_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Program not found")

    payload = {
        "program_name": prog.program_name or existing["Program_Name"],
        "degree_level": prog.degree_level or existing["Degree_Level"],
        "department_id": prog.department_id or existing["Department_ID"]
    }
    model = Program(payload["program_name"], payload["degree_level"], payload["department_id"])
    model.validate()

    execute_commit(
        "UPDATE Program SET Program_Name = ?, Degree_Level = ?, Department_ID = ? WHERE Program_ID = ?",
        (model.program_name, model.degree_level, model.department_id, program_id)
    )
    return {"program_id": program_id, "message": "Program updated successfully"}

@app.delete("/api/programs/{program_id}")
def delete_program(program_id: int):
    if not query_one("SELECT 1 FROM Program WHERE Program_ID = ?", (program_id,)):
        raise HTTPException(status_code=404, detail="Program not found")
    try:
        execute_commit("DELETE FROM Program WHERE Program_ID = ?", (program_id,))
        return {"program_id": program_id, "message": "Program deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 3: STUDENTS & TRANSCRIPT (OOP GPA & ATTENDANCE CALCULATIONS)
# ============================================================================

@app.get("/api/students")
def list_students(program_id: Optional[int] = None):
    query = """
        SELECT s.*, p.Program_Name, d.Department_Name
        FROM Student s
        JOIN Program p ON s.Program_ID = p.Program_ID
        JOIN Department d ON p.Department_ID = d.Department_ID
    """
    params = ()
    if program_id:
        query += " WHERE s.Program_ID = ?"
        params = (program_id,)
    query += " ORDER BY s.Student_ID ASC"
    return query_all(query, params)

@app.post("/api/students")
def create_student(stud: StudentCreate):
    model = Student(
        registration_no=stud.registration_no,
        student_name=stud.student_name,
        email=stud.email,
        phone=stud.phone,
        admission_date=stud.admission_date,
        program_id=stud.program_id
    )
    model.validate()
    try:
        new_id = execute_commit(
            """INSERT INTO Student 
               (Registration_No, Student_Name, Email, Phone, Admission_Date, Program_ID) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (model.registration_no, model.student_name, model.email, model.phone, model.admission_date, model.program_id)
        )
        return {"student_id": new_id, "message": "Student registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/students/{student_id}")
def get_student(student_id: int):
    item = query_one("""
        SELECT s.*, p.Program_Name, d.Department_Name
        FROM Student s
        JOIN Program p ON s.Program_ID = p.Program_ID
        JOIN Department d ON p.Department_ID = d.Department_ID
        WHERE s.Student_ID = ?
    """, (student_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    return item

@app.put("/api/students/{student_id}")
def update_student(student_id: int, stud: StudentUpdate):
    existing = query_one("SELECT * FROM Student WHERE Student_ID = ?", (student_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    payload = {
        "registration_no": stud.registration_no or existing["Registration_No"],
        "student_name": stud.student_name or existing["Student_Name"],
        "email": stud.email or existing["Email"],
        "phone": stud.phone or existing["Phone"],
        "admission_date": stud.admission_date or existing["Admission_Date"],
        "program_id": stud.program_id or existing["Program_ID"]
    }
    model = Student(
        registration_no=payload["registration_no"],
        student_name=payload["student_name"],
        email=payload["email"],
        phone=payload["phone"],
        admission_date=payload["admission_date"],
        program_id=payload["program_id"]
    )
    model.validate()

    execute_commit(
        "UPDATE Student SET Registration_No = ?, Student_Name = ?, Email = ?, Phone = ?, Admission_Date = ?, Program_ID = ? WHERE Student_ID = ?",
        (model.registration_no, model.student_name, model.email, model.phone, model.admission_date, model.program_id, student_id)
    )
    return {"student_id": student_id, "message": "Student updated successfully"}

@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    if not query_one("SELECT 1 FROM Student WHERE Student_ID = ?", (student_id,)):
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        execute_commit("DELETE FROM Student WHERE Student_ID = ?", (student_id,))
        return {"student_id": student_id, "message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/students/{student_id}/profile")
def get_student_profile(student_id: int):
    student = query_one("""
        SELECT s.*, p.Program_Name, p.Degree_Level, d.Department_Name
        FROM Student s
        JOIN Program p ON s.Program_ID = p.Program_ID
        JOIN Department d ON p.Department_ID = d.Department_ID
        WHERE s.Student_ID = ?
    """, (student_id,))
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch results for GPA calculation
    results = query_all("""
        SELECT r.*, e.Exam_Type, e.Total_Marks, c.Course_Code, c.Course_Name, c.Credit_Hours
        FROM Result r
        JOIN Exam e ON r.Exam_ID = e.Exam_ID
        JOIN Course_Offering co ON e.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        WHERE r.Student_ID = ?
    """, (student_id,))

    # Fetch attendance
    attendance_records = query_all("""
        SELECT * FROM Attendance WHERE Student_ID = ?
    """, (student_id,))

    # Utilize OOP Methods in Student domain class
    cgpa = Student.calculate_gpa(results)
    att_pct = Student.calculate_attendance_percentage(attendance_records)

    # Active enrollments
    enrollments = query_all("""
        SELECT en.*, c.Course_Code, c.Course_Name, c.Credit_Hours,
               t.Teacher_Name, sem.Semester_Name, sem.Year, cr.Building_Name, cr.Room_Number
        FROM Enrollment en
        JOIN Course_Offering co ON en.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
        JOIN Semester sem ON co.Semester_ID = sem.Semester_ID
        JOIN Classroom cr ON co.Room_ID = cr.Room_ID
        WHERE en.Student_ID = ?
    """, (student_id,))

    return {
        "student": student,
        "cgpa": cgpa,
        "attendance_rate": att_pct,
        "enrollments": enrollments,
        "results": results,
        "attendance": attendance_records
    }


# ============================================================================
# MODULE 4: TEACHERS / FACULTY
# ============================================================================

@app.get("/api/teachers")
def list_teachers(department_id: Optional[int] = None):
    query = """
        SELECT t.*, d.Department_Name
        FROM Teacher t
        JOIN Department d ON t.Department_ID = d.Department_ID
    """
    params = ()
    if department_id:
        query += " WHERE t.Department_ID = ?"
        params = (department_id,)
    query += " ORDER BY CASE WHEN t.Teacher_Name LIKE '%Khurram%' THEN 0 ELSE 1 END, t.Teacher_ID ASC"
    return query_all(query, params)

@app.post("/api/teachers")
def create_teacher(tch: TeacherCreate):
    model = Teacher(tch.teacher_name, tch.email, tch.phone, tch.designation, tch.department_id)
    model.validate()
    try:
        new_id = execute_commit(
            """INSERT INTO Teacher 
               (Teacher_Name, Email, Phone, Designation, Department_ID) 
               VALUES (?, ?, ?, ?, ?)""",
            (model.teacher_name, model.email, model.phone, model.designation, model.department_id)
        )
        return {"teacher_id": new_id, "message": "Teacher created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/teachers/{teacher_id}")
def get_teacher(teacher_id: int):
    item = query_one("""
        SELECT t.*, d.Department_Name
        FROM Teacher t
        JOIN Department d ON t.Department_ID = d.Department_ID
        WHERE t.Teacher_ID = ?
    """, (teacher_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return item

@app.put("/api/teachers/{teacher_id}")
def update_teacher(teacher_id: int, tch: TeacherUpdate):
    existing = query_one("SELECT * FROM Teacher WHERE Teacher_ID = ?", (teacher_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Teacher not found")

    payload = {
        "teacher_name": tch.teacher_name or existing["Teacher_Name"],
        "email": tch.email or existing["Email"],
        "phone": tch.phone or existing["Phone"],
        "designation": tch.designation or existing["Designation"],
        "department_id": tch.department_id or existing["Department_ID"]
    }
    model = Teacher(payload["teacher_name"], payload["email"], payload["phone"], payload["designation"], payload["department_id"])
    model.validate()

    execute_commit(
        "UPDATE Teacher SET Teacher_Name = ?, Email = ?, Phone = ?, Designation = ?, Department_ID = ? WHERE Teacher_ID = ?",
        (model.teacher_name, model.email, model.phone, model.designation, model.department_id, teacher_id)
    )
    return {"teacher_id": teacher_id, "message": "Teacher updated successfully"}

@app.delete("/api/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    if not query_one("SELECT 1 FROM Teacher WHERE Teacher_ID = ?", (teacher_id,)):
        raise HTTPException(status_code=404, detail="Teacher not found")
    try:
        execute_commit("DELETE FROM Teacher WHERE Teacher_ID = ?", (teacher_id,))
        return {"teacher_id": teacher_id, "message": "Teacher deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 5: COURSES
# ============================================================================

@app.get("/api/courses")
def list_courses(department_id: Optional[int] = None):
    query = """
        SELECT c.*, d.Department_Name
        FROM Course c
        JOIN Department d ON c.Department_ID = d.Department_ID
    """
    params = ()
    if department_id:
        query += " WHERE c.Department_ID = ?"
        params = (department_id,)
    query += " ORDER BY c.Course_ID ASC"
    return query_all(query, params)

@app.post("/api/courses")
def create_course(crs: CourseCreate):
    model = Course(crs.course_code, crs.course_name, crs.credit_hours, crs.department_id, crs.course_description or "")
    model.validate()
    try:
        new_id = execute_commit(
            """INSERT INTO Course 
               (Course_Code, Course_Name, Credit_Hours, Department_ID, Course_Description) 
               VALUES (?, ?, ?, ?, ?)""",
            (model.course_code, model.course_name, model.credit_hours, model.department_id, model.course_description)
        )
        return {"course_id": new_id, "message": "Course created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/courses/{course_id}")
def get_course(course_id: int):
    item = query_one("""
        SELECT c.*, d.Department_Name
        FROM Course c
        JOIN Department d ON c.Department_ID = d.Department_ID
        WHERE c.Course_ID = ?
    """, (course_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Course not found")
    return item

@app.put("/api/courses/{course_id}")
def update_course(course_id: int, crs: CourseUpdate):
    existing = query_one("SELECT * FROM Course WHERE Course_ID = ?", (course_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Course not found")

    payload = {
        "course_code": crs.course_code or existing["Course_Code"],
        "course_name": crs.course_name or existing["Course_Name"],
        "credit_hours": crs.credit_hours if crs.credit_hours is not None else existing["Credit_Hours"],
        "department_id": crs.department_id or existing["Department_ID"],
        "course_description": crs.course_description if crs.course_description is not None else existing["Course_Description"]
    }
    model = Course(payload["course_code"], payload["course_name"], payload["credit_hours"], payload["department_id"], payload["course_description"] or "")
    model.validate()

    execute_commit(
        "UPDATE Course SET Course_Code = ?, Course_Name = ?, Credit_Hours = ?, Department_ID = ?, Course_Description = ? WHERE Course_ID = ?",
        (model.course_code, model.course_name, model.credit_hours, model.department_id, model.course_description, course_id)
    )
    return {"course_id": course_id, "message": "Course updated successfully"}

@app.delete("/api/courses/{course_id}")
def delete_course(course_id: int):
    if not query_one("SELECT 1 FROM Course WHERE Course_ID = ?", (course_id,)):
        raise HTTPException(status_code=404, detail="Course not found")
    try:
        execute_commit("DELETE FROM Course WHERE Course_ID = ?", (course_id,))
        return {"course_id": course_id, "message": "Course deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 6: SEMESTERS
# ============================================================================

@app.get("/api/semesters")
def list_semesters():
    return query_all("SELECT * FROM Semester ORDER BY Year DESC, Semester_Name DESC")

@app.post("/api/semesters")
def create_semester(sem: SemesterCreate):
    model = Semester(sem.semester_name, sem.year, sem.start_date, sem.end_date)
    try:
        new_id = execute_commit(
            "INSERT INTO Semester (Semester_Name, Year, Start_Date, End_Date) VALUES (?, ?, ?, ?)",
            (model.semester_name, model.year, model.start_date, model.end_date)
        )
        return {"semester_id": new_id, "message": "Semester created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/semesters/{semester_id}")
def get_semester(semester_id: int):
    item = query_one("SELECT * FROM Semester WHERE Semester_ID = ?", (semester_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Semester not found")
    return item

@app.put("/api/semesters/{semester_id}")
def update_semester(semester_id: int, sem: SemesterUpdate):
    existing = query_one("SELECT * FROM Semester WHERE Semester_ID = ?", (semester_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Semester not found")

    payload = {
        "semester_name": sem.semester_name or existing["Semester_Name"],
        "year": sem.year if sem.year is not None else existing["Year"],
        "start_date": sem.start_date or existing["Start_Date"],
        "end_date": sem.end_date or existing["End_Date"]
    }
    model = Semester(payload["semester_name"], payload["year"], payload["start_date"], payload["end_date"])

    execute_commit(
        "UPDATE Semester SET Semester_Name = ?, Year = ?, Start_Date = ?, End_Date = ? WHERE Semester_ID = ?",
        (model.semester_name, model.year, model.start_date, model.end_date, semester_id)
    )
    return {"semester_id": semester_id, "message": "Semester updated successfully"}

@app.delete("/api/semesters/{semester_id}")
def delete_semester(semester_id: int):
    if not query_one("SELECT 1 FROM Semester WHERE Semester_ID = ?", (semester_id,)):
        raise HTTPException(status_code=404, detail="Semester not found")
    try:
        execute_commit("DELETE FROM Semester WHERE Semester_ID = ?", (semester_id,))
        return {"semester_id": semester_id, "message": "Semester deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 7: CLASSROOMS
# ============================================================================

@app.get("/api/classrooms")
def list_classrooms():
    return query_all("SELECT * FROM Classroom ORDER BY Building_Name ASC, Room_Number ASC")

@app.post("/api/classrooms")
def create_classroom(cr: ClassroomCreate):
    model = Classroom(cr.building_name, cr.room_number, cr.capacity)
    try:
        new_id = execute_commit(
            "INSERT INTO Classroom (Building_Name, Room_Number, Capacity) VALUES (?, ?, ?)",
            (model.building_name, model.room_number, model.capacity)
        )
        return {"room_id": new_id, "message": "Classroom created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/classrooms/{room_id}")
def get_classroom(room_id: int):
    item = query_one("SELECT * FROM Classroom WHERE Room_ID = ?", (room_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return item

@app.put("/api/classrooms/{room_id}")
def update_classroom(room_id: int, cr: ClassroomUpdate):
    existing = query_one("SELECT * FROM Classroom WHERE Room_ID = ?", (room_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Classroom not found")

    payload = {
        "building_name": cr.building_name or existing["Building_Name"],
        "room_number": cr.room_number or existing["Room_Number"],
        "capacity": cr.capacity if cr.capacity is not None else existing["Capacity"]
    }
    model = Classroom(payload["building_name"], payload["room_number"], payload["capacity"])

    execute_commit(
        "UPDATE Classroom SET Building_Name = ?, Room_Number = ?, Capacity = ? WHERE Room_ID = ?",
        (model.building_name, model.room_number, model.capacity, room_id)
    )
    return {"room_id": room_id, "message": "Classroom updated successfully"}

@app.delete("/api/classrooms/{room_id}")
def delete_classroom(room_id: int):
    if not query_one("SELECT 1 FROM Classroom WHERE Room_ID = ?", (room_id,)):
        raise HTTPException(status_code=404, detail="Classroom not found")
    try:
        execute_commit("DELETE FROM Classroom WHERE Room_ID = ?", (room_id,))
        return {"room_id": room_id, "message": "Classroom deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 8: COURSE OFFERINGS
# ============================================================================

@app.get("/api/offerings")
def list_offerings(semester_id: Optional[int] = None, teacher_id: Optional[int] = None):
    query = """
        SELECT co.*, 
               c.Course_Code, c.Course_Name, c.Credit_Hours,
               s.Semester_Name, s.Year,
               t.Teacher_Name,
               cr.Building_Name, cr.Room_Number, cr.Capacity,
               (SELECT COUNT(*) FROM Enrollment WHERE Offering_ID = co.Offering_ID) AS Enrolled_Count
        FROM Course_Offering co
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Semester s ON co.Semester_ID = s.Semester_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
        JOIN Classroom cr ON co.Room_ID = cr.Room_ID
    """
    params = []
    conditions = []
    if semester_id:
        conditions.append("co.Semester_ID = ?")
        params.append(semester_id)
    if teacher_id:
        conditions.append("co.Teacher_ID = ?")
        params.append(teacher_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY co.Offering_ID DESC"
    return query_all(query, tuple(params))

@app.post("/api/offerings")
def create_offering(off: OfferingCreate):
    model = CourseOffering(off.course_id, off.semester_id, off.teacher_id, off.room_id, off.section or "A")
    try:
        new_id = execute_commit(
            """INSERT INTO Course_Offering 
               (Course_ID, Semester_ID, Teacher_ID, Room_ID, Section) 
               VALUES (?, ?, ?, ?, ?)""",
            (model.course_id, model.semester_id, model.teacher_id, model.room_id, model.section)
        )
        return {"offering_id": new_id, "message": "Course offering created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/offerings/{offering_id}")
def get_offering(offering_id: int):
    item = query_one("""
        SELECT co.*, c.Course_Code, c.Course_Name, s.Semester_Name, s.Year,
               t.Teacher_Name, cr.Building_Name, cr.Room_Number
        FROM Course_Offering co
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Semester s ON co.Semester_ID = s.Semester_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
        JOIN Classroom cr ON co.Room_ID = cr.Room_ID
        WHERE co.Offering_ID = ?
    """, (offering_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Course offering not found")
    return item

@app.put("/api/offerings/{offering_id}")
def update_offering(offering_id: int, off: OfferingUpdate):
    existing = query_one("SELECT * FROM Course_Offering WHERE Offering_ID = ?", (offering_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Course offering not found")

    payload = {
        "course_id": off.course_id or existing["Course_ID"],
        "semester_id": off.semester_id or existing["Semester_ID"],
        "teacher_id": off.teacher_id or existing["Teacher_ID"],
        "room_id": off.room_id or existing["Room_ID"],
        "section": off.section or existing["Section"]
    }
    model = CourseOffering(payload["course_id"], payload["semester_id"], payload["teacher_id"], payload["room_id"], payload["section"])

    execute_commit(
        "UPDATE Course_Offering SET Course_ID = ?, Semester_ID = ?, Teacher_ID = ?, Room_ID = ?, Section = ? WHERE Offering_ID = ?",
        (model.course_id, model.semester_id, model.teacher_id, model.room_id, model.section, offering_id)
    )
    return {"offering_id": offering_id, "message": "Course offering updated successfully"}

@app.delete("/api/offerings/{offering_id}")
def delete_offering(offering_id: int):
    if not query_one("SELECT 1 FROM Course_Offering WHERE Offering_ID = ?", (offering_id,)):
        raise HTTPException(status_code=404, detail="Course offering not found")
    try:
        execute_commit("DELETE FROM Course_Offering WHERE Offering_ID = ?", (offering_id,))
        return {"offering_id": offering_id, "message": "Course offering deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 9: ENROLLMENTS
# ============================================================================

@app.get("/api/enrollments")
def list_enrollments(offering_id: Optional[int] = None, student_id: Optional[int] = None):
    query = """
        SELECT en.*, 
               s.Student_Name, s.Registration_No,
               c.Course_Code, c.Course_Name,
               sem.Semester_Name, sem.Year,
               t.Teacher_Name
        FROM Enrollment en
        JOIN Student s ON en.Student_ID = s.Student_ID
        JOIN Course_Offering co ON en.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Semester sem ON co.Semester_ID = sem.Semester_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
    """
    params = []
    conditions = []
    if offering_id:
        conditions.append("en.Offering_ID = ?")
        params.append(offering_id)
    if student_id:
        conditions.append("en.Student_ID = ?")
        params.append(student_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY en.Enrollment_ID DESC"
    return query_all(query, tuple(params))

@app.post("/api/enrollments")
def create_enrollment(en: EnrollmentCreate):
    existing = query_one(
        "SELECT Enrollment_ID, Status FROM Enrollment WHERE Student_ID = ? AND Offering_ID = ?",
        (en.student_id, en.offering_id)
    )
    if existing:
        if existing["Status"] == "Dropped":
            execute_commit("UPDATE Enrollment SET Status = 'Enrolled', Enrollment_Date = ? WHERE Enrollment_ID = ?", (en.enrollment_date, existing["Enrollment_ID"]))
            return {"enrollment_id": existing["Enrollment_ID"], "message": "Student re-enrolled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Student is already enrolled in this course offering")

    model = Enrollment(en.student_id, en.offering_id, en.enrollment_date, en.status or "Enrolled")
    try:
        new_id = execute_commit(
            "INSERT INTO Enrollment (Student_ID, Offering_ID, Enrollment_Date, Status) VALUES (?, ?, ?, ?)",
            (model.student_id, model.offering_id, model.enrollment_date, model.status)
        )
        return {"enrollment_id": new_id, "message": "Student enrolled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/enrollments/{enrollment_id}")
def get_enrollment(enrollment_id: int):
    item = query_one("""
        SELECT en.*, s.Student_Name, s.Registration_No,
               c.Course_Code, c.Course_Name,
               sem.Semester_Name, sem.Year,
               t.Teacher_Name
        FROM Enrollment en
        JOIN Student s ON en.Student_ID = s.Student_ID
        JOIN Course_Offering co ON en.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Semester sem ON co.Semester_ID = sem.Semester_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
        WHERE en.Enrollment_ID = ?
    """, (enrollment_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return item

@app.put("/api/enrollments/{enrollment_id}")
def update_enrollment(enrollment_id: int, en: EnrollmentUpdate):
    existing = query_one("SELECT * FROM Enrollment WHERE Enrollment_ID = ?", (enrollment_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    payload = {
        "student_id": en.student_id or existing["Student_ID"],
        "offering_id": en.offering_id or existing["Offering_ID"],
        "enrollment_date": en.enrollment_date or existing["Enrollment_Date"],
        "status": en.status or existing["Status"]
    }
    model = Enrollment(payload["student_id"], payload["offering_id"], payload["enrollment_date"], payload["status"])

    execute_commit(
        "UPDATE Enrollment SET Student_ID = ?, Offering_ID = ?, Enrollment_Date = ?, Status = ? WHERE Enrollment_ID = ?",
        (model.student_id, model.offering_id, model.enrollment_date, model.status, enrollment_id)
    )
    return {"enrollment_id": enrollment_id, "message": "Enrollment updated successfully"}

@app.delete("/api/enrollments/{enrollment_id}")
def drop_or_remove_enrollment(enrollment_id: int, permanent: bool = False):
    if not query_one("SELECT 1 FROM Enrollment WHERE Enrollment_ID = ?", (enrollment_id,)):
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if permanent:
        execute_commit("DELETE FROM Enrollment WHERE Enrollment_ID = ?", (enrollment_id,))
        return {"message": "Enrollment permanently removed"}
    else:
        execute_commit("UPDATE Enrollment SET Status = 'Dropped' WHERE Enrollment_ID = ?", (enrollment_id,))
        return {"message": "Enrollment status updated to Dropped"}


# ============================================================================
# MODULE 10: EXAMS
# ============================================================================

@app.get("/api/exams")
def list_exams(offering_id: Optional[int] = None):
    query = """
        SELECT e.*, 
               c.Course_Code, c.Course_Name, co.Section,
               sem.Semester_Name, sem.Year
        FROM Exam e
        JOIN Course_Offering co ON e.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Semester sem ON co.Semester_ID = sem.Semester_ID
    """
    params = ()
    if offering_id:
        query += " WHERE e.Offering_ID = ?"
        params = (offering_id,)
    query += " ORDER BY e.Exam_Date DESC"
    return query_all(query, params)

@app.post("/api/exams")
def create_exam(ex: ExamCreate):
    model = Exam(ex.offering_id, ex.exam_type, ex.exam_date, ex.total_marks)
    try:
        new_id = execute_commit(
            "INSERT INTO Exam (Offering_ID, Exam_Type, Exam_Date, Total_Marks) VALUES (?, ?, ?, ?)",
            (model.offering_id, model.exam_type, model.exam_date, model.total_marks)
        )
        return {"exam_id": new_id, "message": "Exam scheduled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/exams/{exam_id}")
def get_exam(exam_id: int):
    item = query_one("""
        SELECT e.*, c.Course_Code, c.Course_Name, co.Section,
               sem.Semester_Name, sem.Year
        FROM Exam e
        JOIN Course_Offering co ON e.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Semester sem ON co.Semester_ID = sem.Semester_ID
        WHERE e.Exam_ID = ?
    """, (exam_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Exam not found")
    return item

@app.put("/api/exams/{exam_id}")
def update_exam(exam_id: int, ex: ExamUpdate):
    existing = query_one("SELECT * FROM Exam WHERE Exam_ID = ?", (exam_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Exam not found")

    payload = {
        "offering_id": ex.offering_id or existing["Offering_ID"],
        "exam_type": ex.exam_type or existing["Exam_Type"],
        "exam_date": ex.exam_date or existing["Exam_Date"],
        "total_marks": ex.total_marks if ex.total_marks is not None else existing["Total_Marks"]
    }
    model = Exam(payload["offering_id"], payload["exam_type"], payload["exam_date"], payload["total_marks"])

    execute_commit(
        "UPDATE Exam SET Offering_ID = ?, Exam_Type = ?, Exam_Date = ?, Total_Marks = ? WHERE Exam_ID = ?",
        (model.offering_id, model.exam_type, model.exam_date, model.total_marks, exam_id)
    )
    return {"exam_id": exam_id, "message": "Exam updated successfully"}

@app.delete("/api/exams/{exam_id}")
def delete_exam(exam_id: int):
    if not query_one("SELECT 1 FROM Exam WHERE Exam_ID = ?", (exam_id,)):
        raise HTTPException(status_code=404, detail="Exam not found")
    try:
        execute_commit("DELETE FROM Exam WHERE Exam_ID = ?", (exam_id,))
        return {"exam_id": exam_id, "message": "Exam deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MODULE 11: RESULTS
# ============================================================================

@app.get("/api/results")
def list_results(exam_id: Optional[int] = None, student_id: Optional[int] = None):
    query = """
        SELECT r.*,
               s.Student_Name, s.Registration_No,
               e.Exam_Type, e.Total_Marks, e.Exam_Date,
               c.Course_Code, c.Course_Name
        FROM Result r
        JOIN Student s ON r.Student_ID = s.Student_ID
        JOIN Exam e ON r.Exam_ID = e.Exam_ID
        JOIN Course_Offering co ON e.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
    """
    params = []
    conditions = []
    if exam_id:
        conditions.append("r.Exam_ID = ?")
        params.append(exam_id)
    if student_id:
        conditions.append("r.Student_ID = ?")
        params.append(student_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY r.Result_ID DESC"
    return query_all(query, tuple(params))

@app.post("/api/results")
def create_result(res: ResultCreate):
    exam = query_one("SELECT Total_Marks FROM Exam WHERE Exam_ID = ?", (res.exam_id,))
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    total = float(exam["Total_Marks"])
    if res.obtained_marks > total:
        raise HTTPException(status_code=400, detail=f"Obtained marks cannot exceed total marks ({total})")

    grade, grade_point = Result.compute_grade(res.obtained_marks, total)

    existing = query_one("SELECT Result_ID FROM Result WHERE Student_ID = ? AND Exam_ID = ?", (res.student_id, res.exam_id))
    if existing:
        execute_commit(
            "UPDATE Result SET Obtained_Marks = ?, Grade = ?, Grade_Point = ? WHERE Result_ID = ?",
            (res.obtained_marks, grade, grade_point, existing["Result_ID"])
        )
        return {"result_id": existing["Result_ID"], "grade": grade, "grade_point": grade_point, "message": "Result updated successfully"}

    try:
        new_id = execute_commit(
            """INSERT INTO Result 
               (Student_ID, Exam_ID, Obtained_Marks, Grade, Grade_Point) 
               VALUES (?, ?, ?, ?, ?)""",
            (res.student_id, res.exam_id, res.obtained_marks, grade, grade_point)
        )
        return {
            "result_id": new_id,
            "grade": grade,
            "grade_point": grade_point,
            "message": "Result recorded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/results/{result_id}")
def get_result(result_id: int):
    item = query_one("""
        SELECT r.*,
               s.Student_Name, s.Registration_No,
               e.Exam_Type, e.Total_Marks, e.Exam_Date,
               c.Course_Code, c.Course_Name
        FROM Result r
        JOIN Student s ON r.Student_ID = s.Student_ID
        JOIN Exam e ON r.Exam_ID = e.Exam_ID
        JOIN Course_Offering co ON e.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        WHERE r.Result_ID = ?
    """, (result_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Result not found")
    return item

@app.put("/api/results/{result_id}")
def update_result(result_id: int, res: ResultUpdate):
    existing = query_one("SELECT * FROM Result WHERE Result_ID = ?", (result_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Result not found")

    payload = {
        "student_id": res.student_id or existing["Student_ID"],
        "exam_id": res.exam_id or existing["Exam_ID"],
        "obtained_marks": res.obtained_marks if res.obtained_marks is not None else existing["Obtained_Marks"]
    }
    exam = query_one("SELECT Total_Marks FROM Exam WHERE Exam_ID = ?", (payload["exam_id"],))
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    total = float(exam["Total_Marks"])
    if payload["obtained_marks"] > total:
        raise HTTPException(status_code=400, detail=f"Obtained marks cannot exceed total marks ({total})")

    grade, grade_point = Result.compute_grade(payload["obtained_marks"], total)
    execute_commit(
        "UPDATE Result SET Student_ID = ?, Exam_ID = ?, Obtained_Marks = ?, Grade = ?, Grade_Point = ? WHERE Result_ID = ?",
        (payload["student_id"], payload["exam_id"], payload["obtained_marks"], grade, grade_point, result_id)
    )
    return {"result_id": result_id, "grade": grade, "grade_point": grade_point, "message": "Result updated successfully"}

@app.delete("/api/results/{result_id}")
def delete_result(result_id: int):
    if not query_one("SELECT 1 FROM Result WHERE Result_ID = ?", (result_id,)):
        raise HTTPException(status_code=404, detail="Result not found")
    execute_commit("DELETE FROM Result WHERE Result_ID = ?", (result_id,))
    return {"result_id": result_id, "message": "Result deleted successfully"}


# ============================================================================
# MODULE 12: ATTENDANCE
# ============================================================================

@app.get("/api/attendance")
def list_attendance(offering_id: Optional[int] = None, student_id: Optional[int] = None):
    query = """
        SELECT a.*,
               s.Student_Name, s.Registration_No,
               c.Course_Code, c.Course_Name
        FROM Attendance a
        JOIN Student s ON a.Student_ID = s.Student_ID
        JOIN Course_Offering co ON a.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
    """
    params = []
    conditions = []
    if offering_id:
        conditions.append("a.Offering_ID = ?")
        params.append(offering_id)
    if student_id:
        conditions.append("a.Student_ID = ?")
        params.append(student_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY a.Attendance_Date DESC, s.Student_Name ASC"
    return query_all(query, tuple(params))

@app.post("/api/attendance")
def record_attendance(att: AttendanceCreate):
    model = Attendance(att.student_id, att.offering_id, att.attendance_date, att.status)
    existing = query_one("SELECT Attendance_ID FROM Attendance WHERE Student_ID = ? AND Offering_ID = ? AND Attendance_Date = ?", (att.student_id, att.offering_id, att.attendance_date))
    if existing:
        execute_commit("UPDATE Attendance SET Status = ? WHERE Attendance_ID = ?", (model.status, existing["Attendance_ID"]))
        return {"attendance_id": existing["Attendance_ID"], "message": "Attendance updated successfully"}
    try:
        new_id = execute_commit(
            """INSERT INTO Attendance 
               (Student_ID, Offering_ID, Attendance_Date, Status) 
               VALUES (?, ?, ?, ?)""",
            (model.student_id, model.offering_id, model.attendance_date, model.status)
        )
        return {"attendance_id": new_id, "message": "Attendance marked successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/attendance/{attendance_id}")
def get_attendance(attendance_id: int):
    item = query_one("""
        SELECT a.*, s.Student_Name, s.Registration_No,
               c.Course_Code, c.Course_Name
        FROM Attendance a
        JOIN Student s ON a.Student_ID = s.Student_ID
        JOIN Course_Offering co ON a.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        WHERE a.Attendance_ID = ?
    """, (attendance_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return item

@app.put("/api/attendance/{attendance_id}")
def update_attendance(attendance_id: int, att: AttendanceUpdate):
    existing = query_one("SELECT * FROM Attendance WHERE Attendance_ID = ?", (attendance_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    payload = {
        "student_id": att.student_id or existing["Student_ID"],
        "offering_id": att.offering_id or existing["Offering_ID"],
        "attendance_date": att.attendance_date or existing["Attendance_Date"],
        "status": att.status or existing["Status"]
    }
    model = Attendance(payload["student_id"], payload["offering_id"], payload["attendance_date"], payload["status"])

    execute_commit(
        "UPDATE Attendance SET Student_ID = ?, Offering_ID = ?, Attendance_Date = ?, Status = ? WHERE Attendance_ID = ?",
        (model.student_id, model.offering_id, model.attendance_date, model.status, attendance_id)
    )
    return {"attendance_id": attendance_id, "message": "Attendance record updated successfully"}

@app.delete("/api/attendance/{attendance_id}")
def delete_attendance(attendance_id: int):
    if not query_one("SELECT 1 FROM Attendance WHERE Attendance_ID = ?", (attendance_id,)):
        raise HTTPException(status_code=404, detail="Attendance record not found")
    execute_commit("DELETE FROM Attendance WHERE Attendance_ID = ?", (attendance_id,))
    return {"attendance_id": attendance_id, "message": "Attendance record deleted successfully"}


# ============================================================================
# MODULE 13: TIMETABLE & SCHEDULE CONFLICT CHECK
# ============================================================================

@app.get("/api/timetable")
def list_timetable(room_id: Optional[int] = None, offering_id: Optional[int] = None):
    query = """
        SELECT tt.*,
               c.Course_Code, c.Course_Name, co.Section,
               t.Teacher_Name,
               cr.Building_Name, cr.Room_Number
        FROM Timetable tt
        JOIN Course_Offering co ON tt.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
        JOIN Classroom cr ON tt.Room_ID = cr.Room_ID
    """
    params = []
    conditions = []
    if room_id:
        conditions.append("tt.Room_ID = ?")
        params.append(room_id)
    if offering_id:
        conditions.append("tt.Offering_ID = ?")
        params.append(offering_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY CASE tt.Day " \
             "WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3 " \
             "WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6 ELSE 7 END, " \
             "tt.Start_Time ASC"
    return query_all(query, tuple(params))

@app.post("/api/timetable")
def create_timetable_slot(slot: TimetableCreate):
    model = Timetable(slot.offering_id, slot.room_id, slot.day, slot.start_time, slot.end_time)
    
    # Conflict detection query: check if room is already booked on the same day during overlapping hours
    conflict = query_one(
        """
        SELECT tt.Timetable_ID, c.Course_Code, tt.Start_Time, tt.End_Time
        FROM Timetable tt
        JOIN Course_Offering co ON tt.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        WHERE tt.Room_ID = ? AND tt.Day = ?
          AND NOT (tt.End_Time <= ? OR tt.Start_Time >= ?)
        """,
        (model.room_id, model.day, model.start_time, model.end_time)
    )
    if conflict:
        raise HTTPException(
            status_code=409,
            detail=f"Classroom conflict! Room is already booked for {conflict['Course_Code']} ({conflict['Start_Time']} - {conflict['End_Time']})"
        )

    try:
        new_id = execute_commit(
            """INSERT INTO Timetable 
               (Offering_ID, Room_ID, Day, Start_Time, End_Time) 
               VALUES (?, ?, ?, ?, ?)""",
            (model.offering_id, model.room_id, model.day, model.start_time, model.end_time)
        )
        return {"timetable_id": new_id, "message": "Class schedule slot allocated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/timetable/{timetable_id}")
def get_timetable_slot(timetable_id: int):
    item = query_one("""
        SELECT tt.*, c.Course_Code, c.Course_Name, co.Section,
               t.Teacher_Name, cr.Building_Name, cr.Room_Number
        FROM Timetable tt
        JOIN Course_Offering co ON tt.Offering_ID = co.Offering_ID
        JOIN Course c ON co.Course_ID = c.Course_ID
        JOIN Teacher t ON co.Teacher_ID = t.Teacher_ID
        JOIN Classroom cr ON tt.Room_ID = cr.Room_ID
        WHERE tt.Timetable_ID = ?
    """, (timetable_id,))
    if not item:
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    return item

@app.put("/api/timetable/{timetable_id}")
def update_timetable_slot(timetable_id: int, slot: TimetableUpdate):
    existing = query_one("SELECT * FROM Timetable WHERE Timetable_ID = ?", (timetable_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    payload = {
        "offering_id": slot.offering_id or existing["Offering_ID"],
        "room_id": slot.room_id or existing["Room_ID"],
        "day": slot.day or existing["Day"],
        "start_time": slot.start_time or existing["Start_Time"],
        "end_time": slot.end_time or existing["End_Time"]
    }
    model = Timetable(payload["offering_id"], payload["room_id"], payload["day"], payload["start_time"], payload["end_time"])

    execute_commit(
        "UPDATE Timetable SET Offering_ID = ?, Room_ID = ?, Day = ?, Start_Time = ?, End_Time = ? WHERE Timetable_ID = ?",
        (model.offering_id, model.room_id, model.day, model.start_time, model.end_time, timetable_id)
    )
    return {"timetable_id": timetable_id, "message": "Timetable slot updated successfully"}

@app.delete("/api/timetable/{timetable_id}")
def delete_timetable_slot(timetable_id: int):
    if not query_one("SELECT 1 FROM Timetable WHERE Timetable_ID = ?", (timetable_id,)):
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    execute_commit("DELETE FROM Timetable WHERE Timetable_ID = ?", (timetable_id,))
    return {"timetable_id": timetable_id, "message": "Timetable slot deleted successfully"}


# ============================================================================
# MODULE 14: USER ACCOUNTS
# ============================================================================

@app.get("/api/users")
def list_users():
    return query_all("""
        SELECT u.User_ID, u.Username, u.Role, u.Student_ID, u.Teacher_ID,
               s.Student_Name, t.Teacher_Name, u.Created_At
        FROM User_Account u
        LEFT JOIN Student s ON u.Student_ID = s.Student_ID
        LEFT JOIN Teacher t ON u.Teacher_ID = t.Teacher_ID
        ORDER BY u.User_ID ASC
    """)

@app.post("/api/users")
def create_user(user: UserCreate):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    if user.role not in UserAccount.ROLES:
        raise HTTPException(status_code=400, detail=f"Role must be one of: {', '.join(UserAccount.ROLES)}")

    model = UserAccount(user.username, user.password, user.role, user.student_id, user.teacher_id)
    try:
        new_id = execute_commit(
            "INSERT INTO User_Account (Username, Password, Role, Student_ID, Teacher_ID) VALUES (?, ?, ?, ?, ?)",
            (model.username, model.password, model.role, model.student_id, model.teacher_id)
        )
        return {"user_id": new_id, "message": "User account created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    item = query_one("""
        SELECT u.User_ID, u.Username, u.Role, u.Student_ID, u.Teacher_ID,
               s.Student_Name, t.Teacher_Name, u.Created_At
        FROM User_Account u
        LEFT JOIN Student s ON u.Student_ID = s.Student_ID
        LEFT JOIN Teacher t ON u.Teacher_ID = t.Teacher_ID
        WHERE u.User_ID = ?
    """, (user_id,))
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item

@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    existing = query_one("SELECT * FROM User_Account WHERE User_ID = ?", (user_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    payload = {
        "username": user.username or existing["Username"],
        "password": user.password or existing["Password"],
        "role": user.role or existing["Role"],
        "student_id": user.student_id if user.student_id is not None else existing["Student_ID"],
        "teacher_id": user.teacher_id if user.teacher_id is not None else existing["Teacher_ID"]
    }
    if payload["role"] not in UserAccount.ROLES:
        raise HTTPException(status_code=400, detail=f"Role must be one of: {', '.join(UserAccount.ROLES)}")

    if user.password:
        model = UserAccount(payload["username"], payload["password"], payload["role"], payload["student_id"], payload["teacher_id"], is_already_hashed=False)
    else:
        model = UserAccount(payload["username"], existing["Password"], payload["role"], payload["student_id"], payload["teacher_id"], is_already_hashed=True)

    execute_commit(
        "UPDATE User_Account SET Username = ?, Password = ?, Role = ?, Student_ID = ?, Teacher_ID = ? WHERE User_ID = ?",
        (model.username, model.password, model.role, model.student_id, model.teacher_id, user_id)
    )
    return {"user_id": user_id, "message": "User account updated successfully"}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    if not query_one("SELECT 1 FROM User_Account WHERE User_ID = ?", (user_id,)):
        raise HTTPException(status_code=404, detail="User not found")
    execute_commit("DELETE FROM User_Account WHERE User_ID = ?", (user_id,))
    return {"user_id": user_id, "message": "User account deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
