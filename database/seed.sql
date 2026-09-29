-- ============================================================================
-- UNIVERSITY MANAGEMENT SYSTEM (UMS)
-- Real Timetable & Faculty Dataset: GCUF Department of Software Engineering
-- Semester: Fall 2026 | Section: BS(SE) 5th Eve-B
-- Group Members: Syed Ali Zaman, Muhammad Yasir Ali, Muhammad Umer
-- ============================================================================

-- 1. DEPARTMENTS (22 Academic Departments)
INSERT INTO Department (Department_ID, Department_Name, Department_Email) VALUES
(1, 'Department of Software Engineering', 'se@gcuf.edu.pk'),
(2, 'Department of Computer Science', 'cs@gcuf.edu.pk'),
(3, 'Department of Information Technology', 'it@gcuf.edu.pk'),
(4, 'Department of Islamic Studies', 'islamic@gcuf.edu.pk'),
(5, 'Department of Medical Sciences', 'medical@gcuf.edu.pk'),
(6, 'Department of Electrical Engineering', 'ee@gcuf.edu.pk'),
(7, 'Department of Mechanical Technology', 'mech@gcuf.edu.pk'),
(8, 'Department of Physical Sciences & Physics', 'physics@gcuf.edu.pk'),
(9, 'Department of Civil Engineering', 'civil@gcuf.edu.pk'),
(10, 'Department of Chemistry & Biochemistry', 'chem@gcuf.edu.pk'),
(11, 'Department of Mathematics & Statistics', 'math@gcuf.edu.pk'),
(12, 'Department of Business Administration & Management', 'bba@gcuf.edu.pk'),
(13, 'Department of Economics & Finance', 'econ@gcuf.edu.pk'),
(14, 'Department of English Literature & Linguistics', 'english@gcuf.edu.pk'),
(15, 'Department of Pharmacy & Pharmaceutical Sciences', 'pharmacy@gcuf.edu.pk'),
(16, 'Department of Biotechnology & Bioinformatics', 'biotech@gcuf.edu.pk'),
(17, 'Department of Environmental & Earth Sciences', 'env@gcuf.edu.pk'),
(18, 'Department of Mass Communication & Media Studies', 'media@gcuf.edu.pk'),
(19, 'Department of Psychology & Behavioral Sciences', 'psych@gcuf.edu.pk'),
(20, 'Department of Law & Legal Studies', 'law@gcuf.edu.pk'),
(21, 'Department of Fine Arts & Graphic Design', 'finearts@gcuf.edu.pk'),
(22, 'Department of Education & Pedagogy', 'edu@gcuf.edu.pk');

-- 2. PROGRAMS (Academic Degree Programs for All 22 Departments)
INSERT INTO Program (Program_ID, Program_Name, Degree_Level, Department_ID) VALUES
(1, 'BS Software Engineering', 'Undergraduate (BS)', 1),
(2, 'BS Computer Science', 'Undergraduate (BS)', 2),
(3, 'BS Information Technology', 'Undergraduate (BS)', 3),
(4, 'MS Software Engineering', 'Graduate (MS)', 1),
(5, 'MBBS Medical Sciences', 'Undergraduate (BS)', 5),
(6, 'BS Electrical Engineering', 'Undergraduate (BS)', 6),
(7, 'BS Mechanical Technology', 'Undergraduate (BS)', 7),
(8, 'BS Physics & Physical Sciences', 'Undergraduate (BS)', 8),
(9, 'BS Civil Engineering', 'Undergraduate (BS)', 9),
(10, 'BS Applied Chemistry', 'Undergraduate (BS)', 10),
(11, 'BS Mathematics', 'Undergraduate (BS)', 11),
(12, 'BBA Business Administration', 'Undergraduate (BS)', 12),
(13, 'BS Economics & Finance', 'Undergraduate (BS)', 13),
(14, 'BS English Linguistics', 'Undergraduate (BS)', 14),
(15, 'Doctor of Pharmacy (Pharm-D)', 'Graduate (MS)', 15),
(16, 'BS Biotechnology', 'Undergraduate (BS)', 16),
(17, 'BS Environmental Sciences', 'Undergraduate (BS)', 17),
(18, 'BS Mass Communication', 'Undergraduate (BS)', 18),
(19, 'BS Clinical Psychology', 'Undergraduate (BS)', 19),
(20, 'LL.B. Bachelor of Laws', 'Undergraduate (BS)', 20),
(21, 'BS Graphic Design & Fine Arts', 'Undergraduate (BS)', 21),
(22, 'BS Education & Pedagogy', 'Undergraduate (BS)', 22);

-- 3. TEACHERS / FACULTY (Dr. Khurram is HOD SE at Top #1)
INSERT INTO Teacher (Teacher_ID, Teacher_Name, Email, Phone, Designation, Department_ID) VALUES
(1, 'Dr. Khurram', 'dr.khurram@gcuf.edu.pk', '+92-300-7112233', 'HOD & Associate Professor', 1),
(2, 'Dr. Qamar', 'dr.qamar@gcuf.edu.pk', '+92-301-8223344', 'Associate Professor', 1),
(3, 'Mr. Syed Sajjad', 'syed.sajjad@gcuf.edu.pk', '+92-302-9334455', 'Assistant Professor', 1),
(4, 'Mr. Nauman', 'nauman@gcuf.edu.pk', '+92-303-1445566', 'Lecturer', 1),
(5, 'Mr. Noman S', 'noman.s@gcuf.edu.pk', '+92-304-2556677', 'Lecturer', 1),
(6, 'Mr. Talib', 'talib@gcuf.edu.pk', '+92-305-3667788', 'Lecturer', 4),
(7, 'Dr. Farhan Ahmed', 'farhan.med@gcuf.edu.pk', '+92-306-4778899', 'Professor', 5),
(8, 'Engr. Hamza Shah', 'hamza.ee@gcuf.edu.pk', '+92-307-5889900', 'Assistant Professor', 6),
(9, 'Prof. Imran Khan', 'imran.mech@gcuf.edu.pk', '+92-308-6990011', 'Professor', 7),
(10, 'Dr. Saqib Raza', 'saqib.phy@gcuf.edu.pk', '+92-309-7001122', 'Associate Professor', 8),
(11, 'Dr. Tariq Mahmood', 'tariq.civil@gcuf.edu.pk', '+92-310-8112233', 'Professor', 9),
(12, 'Dr. Ayesha Malik', 'ayesha.chem@gcuf.edu.pk', '+92-311-9223344', 'Associate Professor', 10),
(13, 'Prof. Bilal Hassan', 'bilal.math@gcuf.edu.pk', '+92-312-0334455', 'Professor', 11),
(14, 'Dr. Sarah Usman', 'sarah.bba@gcuf.edu.pk', '+92-313-1445566', 'Assistant Professor', 12),
(15, 'Dr. Usman Farooq', 'usman.econ@gcuf.edu.pk', '+92-314-2556677', 'Associate Professor', 13),
(16, 'Prof. Maria Zain', 'maria.eng@gcuf.edu.pk', '+92-315-3667788', 'Professor', 14),
(17, 'Dr. Hassan Ali', 'hassan.pharm@gcuf.edu.pk', '+92-316-4778899', 'Professor', 15),
(18, 'Dr. Rabia Basri', 'rabia.biotech@gcuf.edu.pk', '+92-317-5889900', 'Associate Professor', 16),
(19, 'Dr. Waseem Akram', 'waseem.env@gcuf.edu.pk', '+92-318-6990011', 'Assistant Professor', 17),
(20, 'Prof. Shahida Parveen', 'shahida.media@gcuf.edu.pk', '+92-319-7001122', 'Professor', 18),
(21, 'Dr. Faisal Shah', 'faisal.psych@gcuf.edu.pk', '+92-320-8112233', 'Associate Professor', 19),
(22, 'Adv. Rashid Minhas', 'rashid.law@gcuf.edu.pk', '+92-321-9223344', 'Senior Lecturer', 20);

-- 4. CLASSROOMS & LABS (From Official Timetable)
INSERT INTO Classroom (Room_ID, Building_Name, Room_Number, Capacity) VALUES
(1, 'Sports Block', 'Sports Blk', 60),
(2, 'SE Academic Block', 'SE Lab-2', 45),
(3, 'Research Complex', 'RLab', 50),
(4, 'Main Block', 'Room-1', 55),
(5, 'Main Block', 'Room-2', 50),
(6, 'Main Block', 'Room-3', 50),
(7, 'SE Block', 'SE Hall 2', 70);

-- 5. COURSES (Covering All 22 Departments)
INSERT INTO Course (Course_ID, Course_Code, Course_Name, Credit_Hours, Department_ID, Course_Description) VALUES
(1, 'SDaA', 'Software Design & Architecture Analysis', 4, 1, 'Architectural patterns, domain modeling, 3NF database designs, and system quality attributes.'),
(2, 'HCI & CG', 'Human Computer Interaction & Computer Graphics', 4, 1, 'UI/UX design principles, usability metrics, 2D/3D transformations, and rendering.'),
(3, 'Info. Sec', 'Information Security', 4, 1, 'Threat modeling, encryption, access control, network defense, and secure software development.'),
(4, 'AI', 'Artificial Intelligence', 4, 1, 'Search algorithms, knowledge representation, reasoning, machine learning foundations.'),
(5, 'CO&AL', 'Computer Organization & Assembly Language', 4, 1, 'Instruction set architectures, processor registers, memory hierarchies, and assembly programming.'),
(6, 'Web Eng', 'Web Engineering', 4, 1, 'Full-stack web application development, client-server models, RESTful APIs, and cloud deployments.'),
(7, 'THQ III', 'Translation of the Holy Quran III', 1, 4, 'Recitation, translation, and ethical understanding of Quranic chapters.'),
(8, 'MED-101', 'Anatomy & Physiology', 4, 5, 'Human body structures, physiological systems, and medical diagnostics.'),
(9, 'EE-201', 'Circuit Analysis & Electronics', 4, 6, 'Electrical circuits, semiconductors, signal processing, and hardware design.'),
(10, 'MECH-301', 'Thermodynamics & Robotics', 3, 7, 'Industrial microcontrollers, mechanics, thermal systems, and automation.'),
(11, 'PHY-102', 'General Physics & Kinematics', 3, 8, 'Newtonian mechanics, thermodynamics, electromagnetism, and wave motion.'),
(12, 'CIV-105', 'Structural Mechanics & Surveying', 4, 9, 'Civil construction dynamics, surveying techniques, and structural analysis.'),
(13, 'CHEM-202', 'Organic Chemistry & Analytical Tech', 3, 10, 'Chemical synthesis, molecular structures, and spectroscopy.'),
(14, 'MATH-301', 'Multivariable Calculus & Linear Algebra', 3, 11, 'Vector spaces, matrix transformations, and differential equations.'),
(15, 'MGT-101', 'Principles of Management & Marketing', 3, 12, 'Corporate governance, strategic planning, and brand management.'),
(16, 'ECON-102', 'Microeconomics & Financial Accounting', 3, 13, 'Economic principles, market equilibrium, and balance sheets.'),
(17, 'ENG-101', 'Academic Writing & Linguistics', 3, 14, 'Phonetics, grammar structures, and advanced writing.'),
(18, 'PHARM-201', 'Pharmacology & Medicinal Chemistry', 4, 15, 'Drug interactions, dosage formulation, and medicinal chemistry.'),
(19, 'BIOTECH-301', 'Genomics & Bioinformatics', 4, 16, 'DNA sequencing, genetic algorithms, and molecular biology.'),
(20, 'ENV-101', 'Environmental Ecology & Climate Policy', 3, 17, 'Ecological balance, environmental impact assessment, and sustainability.'),
(21, 'MEDIA-202', 'Digital Journalism & Mass Media', 3, 18, 'News broadcasting, media ethics, and content creation.'),
(22, 'PSYCH-105', 'Behavioral Psychology & Cognitive Science', 3, 19, 'Human behavior, cognitive processing, and mental health studies.');

-- 6. SEMESTER
INSERT INTO Semester (Semester_ID, Semester_Name, Year, Start_Date, End_Date) VALUES
(1, 'Fall', 2026, '2026-09-01', '2027-01-25');

-- 7. STUDENTS (Muhammad Yasir Ali is Top #1 Class Topper & Demo Account)
INSERT INTO Student (Student_ID, Registration_No, Student_Name, Email, Phone, Admission_Date, Program_ID) VALUES
(1, 'FA24-BSE-001', 'Muhammad Yasir Ali', 'yasir.ali@student.gcuf.edu.pk', '+92-322-2345678', '2024-09-01', 1),
(2, 'FA24-BSE-002', 'Syed Ali Zaman', 'ali.zaman@student.gcuf.edu.pk', '+92-321-1234567', '2024-09-01', 1),
(3, 'FA24-BSE-003', 'Muhammad Umer', 'm.umer@student.gcuf.edu.pk', '+92-323-3456789', '2024-09-01', 1),
(4, 'FA24-BSE-014', 'Abdullah Noor', 'abdullah.noor@student.gcuf.edu.pk', '+92-324-4567890', '2024-09-01', 1),
(5, 'FA24-BSE-022', 'Hamza Tariq', 'hamza.tariq@student.gcuf.edu.pk', '+92-325-5678901', '2024-09-01', 1),
(6, 'FA24-BSE-035', 'Ayesha Siddiqua', 'ayesha.s@student.gcuf.edu.pk', '+92-326-6789012', '2024-09-01', 1),
(7, 'FA24-MED-005', 'Bilal Ahmed', 'bilal.med@student.gcuf.edu.pk', '+92-327-7890123', '2024-09-01', 5),
(8, 'FA24-EE-010', 'Zainab Fatima', 'zainab.ee@student.gcuf.edu.pk', '+92-328-8901234', '2024-09-01', 6),
(9, 'FA24-BBA-008', 'Usman Ghani', 'usman.bba@student.gcuf.edu.pk', '+92-329-9012345', '2024-09-01', 12);

-- 8. COURSE OFFERINGS (Offerings Active for All Departments)
INSERT INTO Course_Offering (Offering_ID, Course_ID, Semester_ID, Teacher_ID, Room_ID, Section) VALUES
(1, 1, 1, 1, 3, 'Eve-B'), -- SDaA with Dr. Khurram (HOD SE)
(2, 2, 1, 3, 1, 'Eve-B'), -- HCI & CG with Mr. Syed Sajjad
(3, 3, 1, 4, 1, 'Eve-B'), -- Info. Sec with Mr. Nauman
(4, 4, 1, 3, 1, 'Eve-B'), -- AI with Mr. Syed Sajjad
(5, 5, 1, 2, 4, 'Eve-B'), -- CO&AL with Dr. Qamar
(6, 6, 1, 5, 7, 'Eve-B'), -- Web Eng with Mr. Noman S
(7, 7, 1, 6, 5, 'Eve-B'), -- THQ III with Mr. Talib
(8, 8, 1, 7, 4, 'Sec-A'), -- Medical Anatomy with Dr. Farhan Ahmed
(9, 9, 1, 8, 2, 'Sec-A'), -- EE Electronics with Engr. Hamza Shah
(10, 10, 1, 9, 3, 'Sec-A'), -- Mech Robotics with Prof. Imran Khan
(11, 11, 1, 10, 5, 'Sec-A'), -- Physics with Dr. Saqib Raza
(12, 12, 1, 11, 6, 'Sec-A'), -- Civil Engineering with Dr. Tariq Mahmood
(13, 13, 1, 12, 4, 'Sec-A'), -- Chemistry with Dr. Ayesha Malik
(14, 14, 1, 13, 5, 'Sec-A'), -- Mathematics with Prof. Bilal Hassan
(15, 15, 1, 14, 6, 'Sec-A'), -- BBA Management with Dr. Sarah Usman
(16, 16, 1, 15, 1, 'Sec-A'), -- Economics with Dr. Usman Farooq
(17, 17, 1, 16, 2, 'Sec-A'), -- English with Prof. Maria Zain
(18, 18, 1, 17, 3, 'Sec-A'), -- Pharmacy with Dr. Hassan Ali
(19, 19, 1, 18, 4, 'Sec-A'), -- Biotech with Dr. Rabia Basri
(20, 20, 1, 19, 5, 'Sec-A'), -- Environmental with Dr. Waseem Akram
(21, 21, 1, 20, 6, 'Sec-A'), -- Mass Media with Prof. Shahida Parveen
(22, 22, 1, 21, 7, 'Sec-A'); -- Psychology with Dr. Faisal Shah

-- 9. ENROLLMENTS (All Offerings Enrolled with Full Enroll/Drop/Remove Capabilities)
INSERT INTO Enrollment (Enrollment_ID, Student_ID, Offering_ID, Enrollment_Date, Status) VALUES
-- Muhammad Yasir Ali (Class Topper & Demo Student)
(1, 1, 1, '2026-09-02', 'Enrolled'),
(2, 1, 2, '2026-09-02', 'Enrolled'),
(3, 1, 3, '2026-09-02', 'Enrolled'),
(4, 1, 4, '2026-09-02', 'Enrolled'),
(5, 1, 5, '2026-09-02', 'Enrolled'),
(6, 1, 6, '2026-09-02', 'Enrolled'),
(7, 1, 7, '2026-09-02', 'Enrolled'),
-- Syed Ali Zaman
(8, 2, 1, '2026-09-02', 'Enrolled'),
(9, 2, 2, '2026-09-02', 'Enrolled'),
(10, 2, 3, '2026-09-02', 'Enrolled'),
(11, 2, 4, '2026-09-02', 'Enrolled'),
(12, 2, 5, '2026-09-02', 'Enrolled'),
(13, 2, 6, '2026-09-02', 'Enrolled'),
(14, 2, 7, '2026-09-02', 'Enrolled'),
-- Muhammad Umer
(15, 3, 1, '2026-09-02', 'Enrolled'),
(16, 3, 2, '2026-09-02', 'Enrolled'),
(17, 3, 3, '2026-09-02', 'Enrolled'),
(18, 3, 4, '2026-09-02', 'Enrolled'),
(19, 3, 5, '2026-09-02', 'Enrolled'),
(20, 3, 6, '2026-09-02', 'Enrolled'),
(21, 3, 7, '2026-09-02', 'Enrolled'),
-- Medical Student (Bilal Ahmed)
(22, 7, 8, '2026-09-02', 'Enrolled'),
-- EE Student (Zainab Fatima)
(23, 8, 9, '2026-09-02', 'Enrolled'),
-- BBA Student (Usman Ghani)
(24, 9, 15, '2026-09-02', 'Enrolled');

-- 10. EXAMINATIONS
INSERT INTO Exam (Exam_ID, Offering_ID, Exam_Type, Exam_Date, Total_Marks) VALUES
(1, 1, 'Quiz', '2026-10-15', 20.0),      -- SDaA Quiz
(2, 1, 'Midterm', '2026-11-20', 50.0),   -- SDaA Midterm
(3, 1, 'Final', '2027-01-15', 100.0),    -- SDaA Final
(4, 6, 'Quiz', '2026-10-18', 20.0),      -- Web Eng Quiz
(5, 6, 'Midterm', '2026-11-22', 50.0),   -- Web Eng Midterm
(6, 4, 'Midterm', '2026-11-25', 50.0),   -- AI Midterm
(7, 3, 'Midterm', '2026-11-27', 50.0),   -- Info Sec Midterm
(8, 8, 'Midterm', '2026-11-21', 50.0),   -- Medical Anatomy Midterm
(9, 9, 'Midterm', '2026-11-23', 50.0);   -- EE Midterm

-- 11. RESULTS (Muhammad Yasir Ali is #1 Class Topper)
INSERT INTO Result (Result_ID, Student_ID, Exam_ID, Obtained_Marks, Grade, Grade_Point) VALUES
(1, 1, 1, 20.0, 'A+', 4.00), -- Muhammad Yasir Ali  ← Class Topper
(2, 2, 1, 18.5, 'A+', 4.00), -- Syed Ali Zaman
(3, 3, 1, 18.0, 'A+', 4.00), -- Muhammad Umer
(4, 1, 2, 50.0, 'A+', 4.00), -- Muhammad Yasir Ali  ← Class Topper
(5, 2, 2, 46.0, 'A', 4.00),
(6, 3, 2, 45.5, 'A', 4.00),
(7, 1, 5, 49.5, 'A+', 4.00), -- Muhammad Yasir Ali  ← Class Topper
(8, 2, 5, 45.0, 'A', 4.00),
(9, 3, 5, 44.5, 'A', 4.00),
(10, 1, 6, 49.0, 'A+', 4.00), -- Muhammad Yasir Ali  ← Class Topper
(11, 2, 6, 44.0, 'A', 4.00),
(12, 3, 6, 43.5, 'A', 4.00),
(13, 7, 8, 48.0, 'A+', 4.00), -- Medical Student
(14, 8, 9, 46.5, 'A', 4.00);  -- EE Student

-- 12. ATTENDANCE
INSERT INTO Attendance (Attendance_ID, Student_ID, Offering_ID, Attendance_Date, Status) VALUES
(1, 1, 1, '2026-09-15', 'Present'),
(2, 2, 1, '2026-09-15', 'Present'),
(3, 3, 1, '2026-09-15', 'Present'),
(4, 1, 1, '2026-09-22', 'Present'),
(5, 2, 1, '2026-09-22', 'Present'),
(6, 3, 1, '2026-09-22', 'Present'),
(7, 1, 6, '2026-09-17', 'Present'),
(8, 2, 6, '2026-09-17', 'Present'),
(9, 3, 6, '2026-09-17', 'Present'),
(10, 7, 8, '2026-09-18', 'Present'),
(11, 8, 9, '2026-09-19', 'Present');

-- 13. TIMETABLE
INSERT INTO Timetable (Timetable_ID, Offering_ID, Room_ID, Day, Start_Time, End_Time) VALUES
(1, 2, 1, 'Monday', '14:00:00', '15:00:00'),
(2, 3, 1, 'Monday', '15:00:00', '16:00:00'),
(3, 3, 2, 'Monday', '16:00:00', '18:00:00'),
(4, 4, 1, 'Monday', '18:00:00', '19:00:00'),
(5, 1, 3, 'Tuesday', '15:00:00', '16:00:00'),
(6, 1, 3, 'Tuesday', '16:00:00', '18:00:00'),
(7, 5, 4, 'Tuesday', '18:00:00', '19:00:00'),
(8, 1, 6, 'Wednesday', '13:00:00', '14:00:00'),
(9, 7, 5, 'Wednesday', '14:00:00', '15:00:00'),
(10, 5, 4, 'Wednesday', '15:00:00', '16:00:00'),
(11, 8, 4, 'Thursday', '10:00:00', '12:00:00'),
(12, 9, 2, 'Thursday', '12:00:00', '14:00:00');

-- 14. USER ACCOUNTS (SHA-256 passwords)
INSERT INTO User_Account (User_ID, Username, Password, Role, Student_ID, Teacher_ID) VALUES
(1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrator', NULL, NULL),
(2, 'dr_khurram', '4b706c9a68a514d797c0c29a5bb742617a942ea7eb75cb75ffb892a006ee79d6', 'Teacher', NULL, 1),
(3, 'dr_qamar', '4b706c9a68a514d797c0c29a5bb742617a942ea7eb75cb75ffb892a006ee79d6', 'Teacher', NULL, 2),
(4, 'syed_sajjad', '4b706c9a68a514d797c0c29a5bb742617a942ea7eb75cb75ffb892a006ee79d6', 'Teacher', NULL, 3),
(5, 'yasir_ali', '8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61', 'Student', 1, NULL),
(6, 'ali_zaman', '8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61', 'Student', 2, NULL),
(7, 'm_umer', '8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61', 'Student', 3, NULL);
