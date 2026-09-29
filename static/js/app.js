/**
 * University Management System (UMS) - Frontend Application Logic
 * Group Members: Syed Ali Zaman, Muhammad Yasir Ali, Muhammad Umer
 */

// Application State
const state = {
  currentView: 'dashboard',
  currentUser: {
    role: 'Administrator',
    name: 'Administrator',
    userId: 1,
    studentId: null,
    teacherId: null
  },
  data: {
    stats: {},
    departments: [],
    programs: [],
    students: [],
    teachers: [],
    courses: [],
    semesters: [],
    classrooms: [],
    offerings: [],
    enrollments: [],
    exams: [],
    results: [],
    attendance: [],
    timetable: [],
    users: [],
    schemaInfo: []
  }
};

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  setupNavigation();
  setupRoleSwitcher();
  setupEventListeners();
  loadAllData();
});

function initTheme() {
  // Dark mode only — permanently locked
  localStorage.removeItem('ums_theme');
  document.documentElement.setAttribute('data-theme', 'dark');
}

// ============================================================================
// NAVIGATION & VIEW ROUTING
// ============================================================================
function setupNavigation() {
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetView = link.getAttribute('data-view');
      navigateTo(targetView);
    });
  });
}

function navigateTo(viewId) {
  state.currentView = viewId;

  // Update active state in sidebar
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.toggle('active', link.getAttribute('data-view') === viewId);
  });

  // Switch view containers
  document.querySelectorAll('.view-section').forEach(view => {
    view.classList.toggle('active', view.id === `view-${viewId}`);
  });

  // Update Topbar Title
  const titles = {
    'dashboard': 'Executive Dashboard & System Analytics',
    'student-portal': 'My Student Portal — BS(SE) 5th Eve-B',
    'students': 'Student Directory & Records (3NF)',
    'teachers': 'Faculty & Instructors Management',
    'courses': 'Academic Courses & Curriculum',
    'offerings': 'Course Offerings & Semester Assignments',
    'departments': 'Departments & Degree Programs',
    'classrooms': 'Classrooms & Facilities',
    'enrollments': 'Student Course Enrollments (M:N)',
    'examinations': 'Examinations & Student Results',
    'attendance': 'Class Attendance Tracking',
    'timetable': 'Weekly Timetable & Room Scheduling',
    'users': 'User Accounts & Access Control',
    'schema': '3NF Database Schema Inspector & SQL'
  };

  const pageTitle = document.getElementById('topbarPageTitle');
  if (pageTitle && titles[viewId]) {
    pageTitle.textContent = titles[viewId];
  }

  // Refresh view specific data
  renderCurrentView();
}

// ============================================================================
// DATA FETCHING & API INTEGRATION
// ============================================================================
async function loadAllData() {
  try {
    showLoader(true);
    const [
      stats, depts, progs, students, teachers, courses,
      semesters, classrooms, offerings, enrollments, exams,
      results, attendance, timetable, users, schema
    ] = await Promise.all([
      fetch('/api/stats').then(r => r.json()),
      fetch('/api/departments').then(r => r.json()),
      fetch('/api/programs').then(r => r.json()),
      fetch('/api/students').then(r => r.json()),
      fetch('/api/teachers').then(r => r.json()),
      fetch('/api/courses').then(r => r.json()),
      fetch('/api/semesters').then(r => r.json()),
      fetch('/api/classrooms').then(r => r.json()),
      fetch('/api/offerings').then(r => r.json()),
      fetch('/api/enrollments').then(r => r.json()),
      fetch('/api/exams').then(r => r.json()),
      fetch('/api/results').then(r => r.json()),
      fetch('/api/attendance').then(r => r.json()),
      fetch('/api/timetable').then(r => r.json()),
      fetch('/api/users').then(r => r.json()),
      fetch('/api/schema-info').then(r => r.json())
    ]);

    state.data = {
      stats, departments: depts, programs: progs, students, teachers,
      courses, semesters, classrooms, offerings, enrollments,
      exams, results, attendance, timetable, users, schemaInfo: schema
    };

    updateBadgeCounts();
    renderCurrentView();
  } catch (error) {
    console.error('Failed to load UMS data:', error);
    showToast('Failed to load system data. Ensure server is running.', 'error');
  } finally {
    showLoader(false);
  }
}

function updateBadgeCounts() {
  setElementText('badge-students-count', state.data.students.length);
  setElementText('badge-teachers-count', state.data.teachers.length);
  setElementText('badge-courses-count', state.data.courses.length);
  setElementText('badge-offerings-count', state.data.offerings.length);
  setElementText('badge-enrollments-count', state.data.enrollments.length);
  setElementText('badge-exams-count', state.data.exams.length);
}

function renderCurrentView() {
  switch (state.currentView) {
    case 'dashboard':
      renderDashboard();
      break;
    case 'student-portal':
      renderStudentPortal();
      break;
    case 'students':
      renderStudents();
      break;
    case 'teachers':
      renderTeachers();
      break;
    case 'courses':
      renderCourses();
      break;
    case 'offerings':
      renderOfferings();
      break;
    case 'departments':
      renderDepartments();
      break;
    case 'classrooms':
      renderClassrooms();
      break;
    case 'enrollments':
      renderEnrollments();
      break;
    case 'examinations':
      renderExaminations();
      break;
    case 'attendance':
      renderAttendance();
      break;
    case 'timetable':
      renderTimetable();
      break;
    case 'users':
      renderUsers();
      break;
    case 'schema':
      renderSchemaInspector();
      break;
  }
}

// ============================================================================
// DASHBOARD RENDERING
// ============================================================================
function renderDashboard() {
  const s = state.data.stats || {};
  setElementText('stat-students', s.total_students || 0);
  setElementText('stat-teachers', s.total_teachers || 0);
  setElementText('stat-courses', s.total_courses || 0);
  setElementText('stat-offerings', s.total_offerings || 0);
  setElementText('stat-enrollments', s.total_enrollments || 0);
  setElementText('stat-avg-gpa', (s.average_gpa || 0).toFixed(2));

  // Render recent enrollments
  const recentTable = document.getElementById('dashboardRecentEnrollments');
  if (recentTable) {
    const list = state.data.enrollments.slice(0, 5);
    recentTable.innerHTML = list.map(e => `
      <tr>
        <td>
          <strong style="color:#38bdf8;">${escapeHtml(e.Student_Name)}</strong><br>
          <small style="color:#67e8f9; font-weight:600;">${e.Registration_No}</small>
        </td>
        <td>
          <span class="badge badge-primary">${e.Course_Code}</span> 
          <span style="color:#34d399; font-weight:600; margin-left:6px;">${escapeHtml(e.Course_Name)}</span>
        </td>
        <td style="color:#e2e8f0;">${escapeHtml(e.Semester_Name)} ${e.Year}</td>
        <td style="color:var(--text-muted);">${e.Enrollment_Date}</td>
        <td><span class="badge badge-success">${e.Status}</span></td>
      </tr>
    `).join('') || '<tr><td colspan="5" style="text-align:center;">No recent enrollments</td></tr>';
  }

  // Render department summary
  const deptList = document.getElementById('dashboardDeptList');
  if (deptList) {
    deptList.innerHTML = state.data.departments.map(d => {
      const pCount = state.data.programs.filter(p => p.Department_ID === d.Department_ID).length;
      const tCount = state.data.teachers.filter(t => t.Department_ID === d.Department_ID).length;
      const cCount = state.data.courses.filter(c => c.Department_ID === d.Department_ID).length;
      return `
        <div style="background:var(--bg-card); padding:14px; border-radius:var(--radius-sm); border:1px solid rgba(56, 189, 248, 0.25); margin-bottom:12px; transition:var(--transition); box-shadow:0 2px 8px rgba(0,0,0,0.15);">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#38bdf8; font-size:14px;">${escapeHtml(d.Department_Name)}</strong>
            <span style="font-size:12px; color:#34d399; font-weight:600;">${d.Department_Email}</span>
          </div>
          <div style="display:flex; gap:16px; margin-top:8px; font-size:12.5px;">
            <span style="color:#67e8f9; font-weight:600;">📁 ${pCount} Programs</span>
            <span style="color:#34d399; font-weight:600;">👨‍🏫 ${tCount} Faculty</span>
            <span style="color:#38bdf8; font-weight:600;">📚 ${cCount} Courses</span>
          </div>
        </div>
      `;
    }).join('');
  }
}

// ============================================================================
// STUDENT PORTAL RENDERING
// ============================================================================
function renderStudentPortal() {
  // Find current student or default to Student 1 (Muhammad Yasir Ali)
  const studentId = state.currentUser.studentId || 1;
  const student = state.data.students.find(s => s.Student_ID === studentId) || state.data.students[0];
  if (!student) return;

  setElementText('spStudentName', student.Student_Name);
  setElementText('spRegNo', student.Registration_No);
  setElementText('spProgram', `${student.Program_Name} (${student.Department_Name || 'GCUF'})`);

  // Calculate CGPA from recorded results
  const studResults = state.data.results.filter(r => r.Student_ID === student.Student_ID);
  let totalCredits = 0, totalQP = 0;
  studResults.forEach(r => {
    const c = 4.0;
    totalQP += (r.Grade_Point * c);
    totalCredits += c;
  });
  const cgpa = totalCredits > 0 ? (totalQP / totalCredits).toFixed(2) : "4.00";
  setElementText('spCgpa', cgpa);

  // Attendance rate
  const studAtt = state.data.attendance.filter(a => a.Student_ID === student.Student_ID);
  const presentCount = studAtt.filter(a => a.Status === 'Present' || a.Status === 'Late').length;
  const attRate = studAtt.length > 0 ? ((presentCount / studAtt.length) * 100).toFixed(0) : "100";
  setElementText('spAttendance', `${attRate}%`);

  // Enrolled courses for Section Eve-B
  const tbody = document.getElementById('spCoursesTableBody');
  if (tbody) {
    tbody.innerHTML = state.data.offerings.map(o => `
      <tr>
        <td><span class="badge badge-primary">${escapeHtml(o.Course_Code)}</span></td>
        <td><strong>${escapeHtml(o.Course_Name)}</strong></td>
        <td>${o.Credit_Hours} Cr</td>
        <td>👨‍🏫 ${escapeHtml(o.Teacher_Name)}</td>
        <td>📍 ${escapeHtml(o.Room_Number)} (${escapeHtml(o.Building_Name)})</td>
        <td><span class="badge badge-success">Enrolled</span></td>
      </tr>
    `).join('') || '<tr><td colspan="6" style="text-align:center;">No courses enrolled</td></tr>';
  }

  // Today & upcoming timetable highlights
  const scheduleBox = document.getElementById('spScheduleHighlights');
  if (scheduleBox) {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const todayName = days[new Date().getDay()];
    let displaySlots = state.data.timetable.filter(t => t.Day === todayName);
    let titlePrefix = `Today (${todayName})`;
    if (displaySlots.length === 0) {
      displaySlots = state.data.timetable.filter(t => t.Day === 'Tuesday');
      titlePrefix = 'Upcoming Schedule (Tuesday)';
    }

    scheduleBox.innerHTML = `
      <div style="font-size:12px; font-weight:700; color:var(--secondary); margin-bottom:10px; text-transform:uppercase;">
        📌 ${titlePrefix}
      </div>
      ${displaySlots.map(s => {
        const isLab = (s.Course_Name && s.Course_Name.toLowerCase().includes('lab')) || 
                      (s.Course_Code && s.Course_Code.toLowerCase().includes('lab'));
        return `
          <div style="background:var(--bg-main); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:10px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>${escapeHtml(s.Course_Code)} - ${escapeHtml(s.Course_Name)}</strong>
              <span class="badge ${isLab ? 'badge-info' : 'badge-primary'}">${s.Start_Time.slice(0,5)} - ${s.End_Time.slice(0,5)}</span>
            </div>
            <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">
              👨‍🏫 ${escapeHtml(s.Teacher_Name)} &bull; 📍 ${escapeHtml(s.Room_Number)} (${escapeHtml(s.Building_Name)})
            </div>
          </div>
        `;
      }).join('')}
    `;
  }
}

// ============================================================================
// STUDENTS RENDERING & TRANSCRIPT MODAL
// ============================================================================
function renderStudents(filterText = '') {
  const tbody = document.getElementById('studentsTableBody');
  if (!tbody) return;

  const query = filterText.toLowerCase();
  const filtered = state.data.students.filter(s =>
    s.Student_Name.toLowerCase().includes(query) ||
    s.Registration_No.toLowerCase().includes(query) ||
    s.Email.toLowerCase().includes(query) ||
    s.Program_Name.toLowerCase().includes(query)
  );

  tbody.innerHTML = filtered.map(s => `
    <tr>
      <td><strong>${s.Student_ID}</strong></td>
      <td><span class="badge badge-primary">${escapeHtml(s.Registration_No)}</span></td>
      <td><strong>${escapeHtml(s.Student_Name)}</strong></td>
      <td>${escapeHtml(s.Program_Name)}</td>
      <td>${escapeHtml(s.Email)}</td>
      <td>${escapeHtml(s.Phone)}</td>
      <td>${s.Admission_Date}</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="openStudentTranscript(${s.Student_ID})">
          🎓 Transcript & GPA
        </button>
      </td>
    </tr>
  `).join('') || '<tr><td colspan="8" style="text-align:center;">No students found</td></tr>';
}

async function openStudentTranscript(studentId) {
  try {
    showLoader(true);
    const res = await fetch(`/api/students/${studentId}/profile`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to load profile');

    const s = data.student;
    document.getElementById('transcriptStudentName').textContent = s.Student_Name;
    document.getElementById('transcriptRegNo').textContent = s.Registration_No;
    document.getElementById('transcriptProgram').textContent = `${s.Program_Name} (${s.Department_Name})`;
    document.getElementById('transcriptGpaVal').textContent = `CGPA: ${data.cgpa.toFixed(2)}`;
    document.getElementById('transcriptAttendanceVal').textContent = `Attendance: ${data.attendance_rate}%`;

    // Enrolled Courses Table
    const crsBody = document.getElementById('transcriptCoursesBody');
    crsBody.innerHTML = data.enrollments.map(en => `
      <tr>
        <td><strong>${en.Course_Code}</strong></td>
        <td>${escapeHtml(en.Course_Name)}</td>
        <td>${en.Credit_Hours} Cr</td>
        <td>${escapeHtml(en.Teacher_Name)}</td>
        <td>${escapeHtml(en.Semester_Name)} ${en.Year}</td>
        <td><span class="badge ${en.Status === 'Enrolled' ? 'badge-success' : 'badge-danger'}">${en.Status}</span></td>
        <td>
          <button class="btn btn-danger btn-sm" onclick="removeEnrollmentFromProfile(${en.Enrollment_ID}, ${studentId})">🗑️ Remove</button>
        </td>
      </tr>
    `).join('') || '<tr><td colspan="7" style="text-align:center;">No course enrollments</td></tr>';

    // Exam Results Table
    const resBody = document.getElementById('transcriptResultsBody');
    resBody.innerHTML = data.results.map(r => `
      <tr>
        <td>${r.Course_Code}</td>
        <td><span class="badge badge-info">${r.Exam_Type}</span></td>
        <td>${r.Obtained_Marks} / ${r.Total_Marks}</td>
        <td><strong>${r.Grade}</strong></td>
        <td><strong>${r.Grade_Point.toFixed(2)}</strong></td>
      </tr>
    `).join('') || '<tr><td colspan="5" style="text-align:center;">No exam results recorded</td></tr>';

    openModal('studentTranscriptModal');
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    showLoader(false);
  }
}

// ============================================================================
// FACULTY / TEACHERS RENDERING
// ============================================================================
function renderTeachers(filterText = '') {
  const tbody = document.getElementById('teachersTableBody');
  if (!tbody) return;

  const query = filterText.toLowerCase();
  const filtered = state.data.teachers.filter(t =>
    t.Teacher_Name.toLowerCase().includes(query) ||
    t.Email.toLowerCase().includes(query) ||
    t.Designation.toLowerCase().includes(query) ||
    t.Department_Name.toLowerCase().includes(query)
  );

  tbody.innerHTML = filtered.map(t => `
    <tr>
      <td><strong>${t.Teacher_ID}</strong></td>
      <td><strong>${escapeHtml(t.Teacher_Name)}</strong></td>
      <td><span class="badge badge-warning">${escapeHtml(t.Designation)}</span></td>
      <td>${escapeHtml(t.Department_Name)}</td>
      <td>${escapeHtml(t.Email)}</td>
      <td>${escapeHtml(t.Phone)}</td>
    </tr>
  `).join('') || '<tr><td colspan="6" style="text-align:center;">No teachers found</td></tr>';
}

// ============================================================================
// COURSES RENDERING
// ============================================================================
function renderCourses(filterText = '') {
  const tbody = document.getElementById('coursesTableBody');
  if (!tbody) return;

  const query = filterText.toLowerCase();
  const filtered = state.data.courses.filter(c =>
    c.Course_Code.toLowerCase().includes(query) ||
    c.Course_Name.toLowerCase().includes(query) ||
    c.Department_Name.toLowerCase().includes(query)
  );

  tbody.innerHTML = filtered.map(c => `
    <tr>
      <td><strong>${c.Course_ID}</strong></td>
      <td><span class="badge badge-primary">${escapeHtml(c.Course_Code)}</span></td>
      <td><strong>${escapeHtml(c.Course_Name)}</strong></td>
      <td><strong>${c.Credit_Hours}</strong></td>
      <td>${escapeHtml(c.Department_Name)}</td>
      <td style="color:var(--text-muted); font-size:12px;">${escapeHtml(c.Course_Description || '—')}</td>
    </tr>
  `).join('') || '<tr><td colspan="6" style="text-align:center;">No courses found</td></tr>';
}

// ============================================================================
// COURSE OFFERINGS RENDERING
// ============================================================================
function renderOfferings() {
  const tbody = document.getElementById('offeringsTableBody');
  if (!tbody) return;

  tbody.innerHTML = state.data.offerings.map(o => `
    <tr>
      <td><strong>#${o.Offering_ID}</strong></td>
      <td><span class="badge badge-primary">${escapeHtml(o.Course_Code)}</span> <strong>${escapeHtml(o.Course_Name)}</strong></td>
      <td><span class="badge badge-info">Sec ${escapeHtml(o.Section)}</span></td>
      <td>${escapeHtml(o.Semester_Name)} ${o.Year}</td>
      <td>👨‍🏫 ${escapeHtml(o.Teacher_Name)}</td>
      <td>🏛️ ${escapeHtml(o.Building_Name)} - ${escapeHtml(o.Room_Number)}</td>
      <td><span class="badge badge-success">${o.Enrolled_Count} Enrolled</span></td>
    </tr>
  `).join('') || '<tr><td colspan="7" style="text-align:center;">No offerings scheduled</td></tr>';
}

// ============================================================================
// DEPARTMENTS & PROGRAMS RENDERING
// ============================================================================
function renderDepartments() {
  const deptTbody = document.getElementById('departmentsTableBody');
  if (deptTbody) {
    deptTbody.innerHTML = state.data.departments.map(d => `
      <tr>
        <td><strong>${d.Department_ID}</strong></td>
        <td><strong>${escapeHtml(d.Department_Name)}</strong></td>
        <td>${escapeHtml(d.Department_Email)}</td>
        <td>${d.Created_At}</td>
      </tr>
    `).join('');
  }

  const progTbody = document.getElementById('programsTableBody');
  if (progTbody) {
    progTbody.innerHTML = state.data.programs.map(p => `
      <tr>
        <td><strong>${p.Program_ID}</strong></td>
        <td><strong>${escapeHtml(p.Program_Name)}</strong></td>
        <td><span class="badge badge-info">${escapeHtml(p.Degree_Level)}</span></td>
        <td>${escapeHtml(p.Department_Name)}</td>
      </tr>
    `).join('');
  }
}

// ============================================================================
// CLASSROOMS RENDERING
// ============================================================================
function renderClassrooms() {
  const tbody = document.getElementById('classroomsTableBody');
  if (!tbody) return;

  tbody.innerHTML = state.data.classrooms.map(cr => `
    <tr>
      <td><strong>${cr.Room_ID}</strong></td>
      <td>🏛️ ${escapeHtml(cr.Building_Name)}</td>
      <td><strong>${escapeHtml(cr.Room_Number)}</strong></td>
      <td><span class="badge badge-primary">${cr.Capacity} Seats</span></td>
    </tr>
  `).join('');
}

// ============================================================================
// ENROLLMENTS RENDERING
// ============================================================================
function renderEnrollments() {
  const tbody = document.getElementById('enrollmentsTableBody');
  if (!tbody) return;

  tbody.innerHTML = state.data.enrollments.map(en => `
    <tr>
      <td><strong>#${en.Enrollment_ID}</strong></td>
      <td><strong>${escapeHtml(en.Student_Name)}</strong><br><small style="color:var(--text-muted)">${en.Registration_No}</small></td>
      <td><span class="badge badge-primary">${en.Course_Code}</span> ${escapeHtml(en.Course_Name)}</td>
      <td>${escapeHtml(en.Semester_Name)} ${en.Year}</td>
      <td>${en.Enrollment_Date}</td>
      <td>
        <span class="badge ${en.Status === 'Enrolled' ? 'badge-success' : 'badge-danger'}">
          ${en.Status}
        </span>
      </td>
      <td>
        <div style="display:flex; gap:6px;">
          ${en.Status === 'Enrolled' ? `
            <button class="btn btn-secondary btn-sm" onclick="dropEnrollment(${en.Enrollment_ID})">Drop</button>
          ` : ''}
          <button class="btn btn-danger btn-sm" onclick="removeEnrollment(${en.Enrollment_ID})">🗑️ Remove</button>
        </div>
      </td>
    </tr>
  `).join('');
}

async function dropEnrollment(enrollmentId) {
  if (!confirm('Are you sure you want to drop this student enrollment?')) return;
  try {
    const res = await fetch(`/api/enrollments/${enrollmentId}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Enrollment dropped', 'success');
      loadAllData();
    }
  } catch (err) {
    showToast('Failed to drop enrollment', 'error');
  }
}

async function removeEnrollment(enrollmentId) {
  if (!confirm('Are you sure you want to PERMANENTLY remove this student from the subject enrollment?')) return;
  try {
    const res = await fetch(`/api/enrollments/${enrollmentId}?permanent=true`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Student removed from subject enrollment', 'success');
      loadAllData();
    } else {
      const data = await res.json();
      showToast(data.detail || 'Failed to remove enrollment', 'error');
    }
  } catch (err) {
    showToast('Failed to remove enrollment', 'error');
  }
}

async function removeEnrollmentFromProfile(enrollmentId, studentId) {
  if (!confirm('Remove student from this subject enrollment?')) return;
  try {
    const res = await fetch(`/api/enrollments/${enrollmentId}?permanent=true`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Student removed from subject enrollment', 'success');
      await viewStudentProfile(studentId);
      await loadAllData();
    } else {
      const data = await res.json();
      showToast(data.detail || 'Failed to remove enrollment', 'error');
    }
  } catch (err) {
    showToast('Failed to remove enrollment', 'error');
  }
}

// ============================================================================
// EXAMINATIONS & RESULTS RENDERING
// ============================================================================
function renderExaminations() {
  const examsTbody = document.getElementById('examsTableBody');
  if (examsTbody) {
    examsTbody.innerHTML = state.data.exams.map(e => `
      <tr>
        <td><strong>#${e.Exam_ID}</strong></td>
        <td><span class="badge badge-primary">${e.Course_Code}</span> ${escapeHtml(e.Course_Name)} (Sec ${e.Section})</td>
        <td><span class="badge badge-warning">${escapeHtml(e.Exam_Type)}</span></td>
        <td>${e.Exam_Date}</td>
        <td><strong>${e.Total_Marks} Marks</strong></td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openRecordResultModal(${e.Exam_ID}, ${e.Total_Marks})">
            ✍️ Record Marks
          </button>
        </td>
      </tr>
    `).join('');
  }

  const resultsTbody = document.getElementById('resultsTableBody');
  if (resultsTbody) {
    resultsTbody.innerHTML = state.data.results.map(r => `
      <tr>
        <td><strong>${escapeHtml(r.Student_Name)}</strong><br><small style="color:var(--text-muted)">${r.Registration_No}</small></td>
        <td>${r.Course_Code}</td>
        <td><span class="badge badge-info">${r.Exam_Type}</span></td>
        <td><strong>${r.Obtained_Marks}</strong> / ${r.Total_Marks}</td>
        <td><span class="badge badge-success">${r.Grade}</span></td>
        <td><strong>${r.Grade_Point.toFixed(2)}</strong></td>
      </tr>
    `).join('');
  }
}

// ============================================================================
// ATTENDANCE RENDERING
// ============================================================================
function renderAttendance() {
  const tbody = document.getElementById('attendanceTableBody');
  if (!tbody) return;

  tbody.innerHTML = state.data.attendance.map(a => {
    let badgeClass = 'badge-success';
    if (a.Status === 'Absent') badgeClass = 'badge-danger';
    else if (a.Status === 'Late') badgeClass = 'badge-warning';

    return `
      <tr>
        <td><strong>#${a.Attendance_ID}</strong></td>
        <td><strong>${escapeHtml(a.Student_Name)}</strong><br><small style="color:var(--text-muted)">${a.Registration_No}</small></td>
        <td><span class="badge badge-primary">${a.Course_Code}</span> ${escapeHtml(a.Course_Name)}</td>
        <td>${a.Attendance_Date}</td>
        <td><span class="badge ${badgeClass}">${a.Status}</span></td>
      </tr>
    `;
  }).join('');
}

// ============================================================================
// TIMETABLE RENDERING (VISUAL SCHEDULE GRID)
// ============================================================================
function renderTimetable() {
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  const grid = document.getElementById('timetableGridContainer');
  if (!grid) return;

  grid.innerHTML = days.map(day => {
    const slots = state.data.timetable.filter(t => t.Day === day);
    const slotsHtml = slots.map(s => {
      const isLab = (s.Course_Name && s.Course_Name.toLowerCase().includes('lab')) || 
                    (s.Course_Code && s.Course_Code.toLowerCase().includes('lab')) ||
                    (s.Room_Number && s.Room_Number.toLowerCase().includes('lab'));
      return `
        <div class="slot-card" style="${isLab ? 'background:rgba(6, 182, 212, 0.12); border-color:rgba(6, 182, 212, 0.35);' : ''}">
          <div class="slot-time" style="${isLab ? 'color:#67e8f9;' : ''}">⏰ ${s.Start_Time.slice(0, 5)} - ${s.End_Time.slice(0, 5)}</div>
          <div class="slot-course" style="font-weight:700;">
            ${escapeHtml(s.Course_Code)}
            ${isLab ? '<span class="badge badge-info" style="font-size:10px; margin-left:4px;">LAB</span>' : ''}
          </div>
          <div style="font-size:11px; color:var(--text-main); margin:2px 0;">${escapeHtml(s.Course_Name)}</div>
          <div class="slot-instructor">👨‍🏫 ${escapeHtml(s.Teacher_Name)}</div>
          <div class="slot-room" style="margin-top:2px;">📍 ${escapeHtml(s.Room_Number)} (${escapeHtml(s.Building_Name)})</div>
        </div>
      `;
    }).join('') || '<div style="color:var(--text-dim); font-size:12px; text-align:center; padding:12px;">No classes scheduled</div>';

    return `
      <div class="day-column">
        <div class="day-header" style="display:flex; justify-content:space-between; align-items:center;">
          <span>${day}</span>
          <span class="badge badge-primary" style="font-size:10px;">${slots.length} slots</span>
        </div>
        ${slotsHtml}
      </div>
    `;
  }).join('');
}

// ============================================================================
// USER ACCOUNTS RENDERING
// ============================================================================
function renderUsers() {
  const tbody = document.getElementById('usersTableBody');
  if (!tbody) return;

  tbody.innerHTML = state.data.users.map(u => {
    let roleClass = 'badge-primary';
    if (u.Role === 'Teacher') roleClass = 'badge-warning';
    else if (u.Role === 'Student') roleClass = 'badge-info';

    const linked = u.Student_Name ? `Student: ${escapeHtml(u.Student_Name)}` :
                   u.Teacher_Name ? `Faculty: ${escapeHtml(u.Teacher_Name)}` : 'System Superuser';

    return `
      <tr>
        <td><strong>${u.User_ID}</strong></td>
        <td><strong>${escapeHtml(u.Username)}</strong></td>
        <td><span class="badge ${roleClass}">${u.Role}</span></td>
        <td>${linked}</td>
        <td>${u.Created_At}</td>
      </tr>
    `;
  }).join('');
}

// ============================================================================
// 3NF SCHEMA INSPECTOR & LIVE SQL RUNNER
// ============================================================================
function renderSchemaInspector() {
  const container = document.getElementById('schemaTablesContainer');
  if (!container) return;

  container.innerHTML = state.data.schemaInfo.map(t => `
    <div class="card" style="margin-bottom:16px;">
      <div class="card-header" style="background:var(--bg-card); cursor:pointer;" onclick="toggleSchemaTableDetails('${t.table_name}')">
        <div class="card-title">
          <span class="badge badge-primary">Table</span>
          <strong>${t.table_name}</strong>
          <span style="font-size:12px; color:var(--text-muted);">(${t.columns.length} columns)</span>
        </div>
        <div>
          <span class="badge badge-success">${t.row_count} Records</span>
        </div>
      </div>
      <div id="schema-details-${t.table_name}" style="padding:16px; display:block;">
        <div style="font-size:12px; font-weight:600; color:var(--text-muted); margin-bottom:8px;">Columns & Constraints:</div>
        <div class="table-responsive">
          <table style="font-size:12px;">
            <thead>
              <tr>
                <th>Column Name</th>
                <th>Type</th>
                <th>PK</th>
                <th>Not Null</th>
                <th>Default</th>
              </tr>
            </thead>
            <tbody>
              ${t.columns.map(c => `
                <tr>
                  <td><strong>${c.name}</strong></td>
                  <td><code>${c.type}</code></td>
                  <td>${c.pk ? '<span class="badge badge-warning">PRIMARY KEY</span>' : '—'}</td>
                  <td>${c.notnull ? 'Yes' : 'No'}</td>
                  <td>${c.dflt_value || 'NULL'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
        ${t.foreign_keys.length > 0 ? `
          <div style="margin-top:12px; font-size:12px; color:var(--secondary);">
            <strong>Foreign Key References:</strong>
            ${t.foreign_keys.map(fk => `<span>FK: <code>${fk.from}</code> ➔ <code>${fk.table}(${fk.to})</code></span>`).join(' | ')}
          </div>
        ` : ''}
      </div>
    </div>
  `).join('');
}

function toggleSchemaTableDetails(tableName) {
  const el = document.getElementById(`schema-details-${tableName}`);
  if (el) {
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
  }
}

// ============================================================================
// ROLE SWITCHER (FOR LECTURER DEMO)
// ============================================================================
function setupRoleSwitcher() {
  const switcher = document.getElementById('roleSwitcher');
  if (!switcher) return;

  switcher.addEventListener('change', (e) => {
    const val = e.target.value;
    if (val === 'admin') {
      state.currentUser = { role: 'Administrator', name: 'Administrator', userId: 1 };
      navigateTo('dashboard');
    } else if (val === 'teacher') {
      state.currentUser = { role: 'Teacher', name: 'Dr. Khurram (HOD SE)', userId: 2, teacherId: 1 };
      navigateTo('timetable');
    } else if (val === 'student') {
      state.currentUser = { role: 'Student', name: 'Muhammad Yasir Ali', userId: 5, studentId: 1 };
      navigateTo('student-portal');
    }
    updateUserDisplay();
    showToast(`Switched view to ${state.currentUser.role} mode (${state.currentUser.name})`, 'info');
  });
}

function updateUserDisplay() {
  setElementText('currentUserName', state.currentUser.name);
  setElementText('currentUserRole', state.currentUser.role);
}

// ============================================================================
// MODAL MANAGEMENT & FORM HANDLERS
// ============================================================================
function setupEventListeners() {
  // Reset database button
  document.getElementById('resetDbBtn')?.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to reset the database with fresh seed data?')) return;
    try {
      showLoader(true);
      const res = await fetch('/api/reset-db', { method: 'POST' });
      if (res.ok) {
        showToast('Database reset and re-seeded successfully!', 'success');
        await loadAllData();
      }
    } catch (err) {
      showToast('Reset failed', 'error');
    } finally {
      showLoader(false);
    }
  });

  // Search input filters
  setupSearchFilter('studentSearchInput', renderStudents);
  setupSearchFilter('teacherSearchInput', renderTeachers);
  setupSearchFilter('courseSearchInput', renderCourses);

  // Forms submission
  document.getElementById('addStudentForm')?.addEventListener('submit', handleAddStudent);
  document.getElementById('addTeacherForm')?.addEventListener('submit', handleAddTeacher);
  document.getElementById('addCourseForm')?.addEventListener('submit', handleAddCourse);
  document.getElementById('addOfferingForm')?.addEventListener('submit', handleAddOffering);
  document.getElementById('addEnrollmentForm')?.addEventListener('submit', handleAddEnrollment);
  document.getElementById('addExamForm')?.addEventListener('submit', handleAddExam);
  document.getElementById('recordResultForm')?.addEventListener('submit', handleRecordResult);
  document.getElementById('markAttendanceForm')?.addEventListener('submit', handleMarkAttendance);
  document.getElementById('addTimetableForm')?.addEventListener('submit', handleAddTimetable);
}

function setupSearchFilter(inputId, renderFn) {
  const input = document.getElementById(inputId);
  if (input) {
    input.addEventListener('input', (e) => renderFn(e.target.value));
  }
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

// Form Handlers
async function handleAddStudent(e) {
  e.preventDefault();
  const payload = {
    registration_no: document.getElementById('newStudRegNo').value,
    student_name: document.getElementById('newStudName').value,
    email: document.getElementById('newStudEmail').value,
    phone: document.getElementById('newStudPhone').value,
    admission_date: document.getElementById('newStudDate').value,
    program_id: parseInt(document.getElementById('newStudProg').value)
  };
  await submitApiPost('/api/students', payload, 'Student registered successfully', 'addStudentModal');
}

async function handleAddTeacher(e) {
  e.preventDefault();
  const payload = {
    teacher_name: document.getElementById('newTeachName').value,
    email: document.getElementById('newTeachEmail').value,
    phone: document.getElementById('newTeachPhone').value,
    designation: document.getElementById('newTeachDesig').value,
    department_id: parseInt(document.getElementById('newTeachDept').value)
  };
  await submitApiPost('/api/teachers', payload, 'Teacher created successfully', 'addTeacherModal');
}

async function handleAddCourse(e) {
  e.preventDefault();
  const payload = {
    course_code: document.getElementById('newCrsCode').value,
    course_name: document.getElementById('newCrsName').value,
    credit_hours: parseInt(document.getElementById('newCrsCredits').value),
    department_id: parseInt(document.getElementById('newCrsDept').value),
    course_description: document.getElementById('newCrsDesc').value
  };
  await submitApiPost('/api/courses', payload, 'Course created successfully', 'addCourseModal');
}

async function handleAddOffering(e) {
  e.preventDefault();
  const payload = {
    course_id: parseInt(document.getElementById('newOffCourse').value),
    semester_id: parseInt(document.getElementById('newOffSemester').value),
    teacher_id: parseInt(document.getElementById('newOffTeacher').value),
    room_id: parseInt(document.getElementById('newOffRoom').value),
    section: document.getElementById('newOffSection').value || 'A'
  };
  await submitApiPost('/api/offerings', payload, 'Course offering created successfully', 'addOfferingModal');
}

async function handleAddEnrollment(e) {
  e.preventDefault();
  const payload = {
    student_id: parseInt(document.getElementById('newEnStudent').value),
    offering_id: parseInt(document.getElementById('newEnOffering').value),
    enrollment_date: new Date().toISOString().slice(0, 10),
    status: 'Enrolled'
  };
  await submitApiPost('/api/enrollments', payload, 'Student enrolled successfully', 'addEnrollmentModal');
}

async function handleAddExam(e) {
  e.preventDefault();
  const payload = {
    offering_id: parseInt(document.getElementById('newExamOffering').value),
    exam_type: document.getElementById('newExamType').value,
    exam_date: document.getElementById('newExamDate').value,
    total_marks: parseFloat(document.getElementById('newExamTotal').value)
  };
  await submitApiPost('/api/exams', payload, 'Exam scheduled successfully', 'addExamModal');
}

function openRecordResultModal(examId, totalMarks) {
  document.getElementById('resultExamId').value = examId;
  document.getElementById('resultTotalMarksDisplay').textContent = `${totalMarks} Marks`;
  populateSelect('resultStudentSelect', state.data.students, 'Student_ID', s => `${s.Student_Name} (${s.Registration_No})`);
  openModal('recordResultModal');
}

async function handleRecordResult(e) {
  e.preventDefault();
  const payload = {
    exam_id: parseInt(document.getElementById('resultExamId').value),
    student_id: parseInt(document.getElementById('resultStudentSelect').value),
    obtained_marks: parseFloat(document.getElementById('resultObtainedMarks').value)
  };
  await submitApiPost('/api/results', payload, 'Result recorded successfully', 'recordResultModal');
}

async function handleMarkAttendance(e) {
  e.preventDefault();
  const payload = {
    offering_id: parseInt(document.getElementById('attOfferingSelect').value),
    student_id: parseInt(document.getElementById('attStudentSelect').value),
    attendance_date: document.getElementById('attDate').value,
    status: document.getElementById('attStatusSelect').value
  };
  await submitApiPost('/api/attendance', payload, 'Attendance logged successfully', 'markAttendanceModal');
}

async function handleAddTimetable(e) {
  e.preventDefault();
  const payload = {
    offering_id: parseInt(document.getElementById('ttOfferingSelect').value),
    room_id: parseInt(document.getElementById('ttRoomSelect').value),
    day: document.getElementById('ttDaySelect').value,
    start_time: document.getElementById('ttStartTime').value,
    end_time: document.getElementById('ttEndTime').value
  };
  await submitApiPost('/api/timetable', payload, 'Timetable slot assigned successfully', 'addTimetableModal');
}

async function submitApiPost(url, payload, successMsg, modalToClose) {
  try {
    showLoader(true);
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');
    showToast(successMsg, 'success');
    if (modalToClose) closeModal(modalToClose);
    await loadAllData();
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    showLoader(false);
  }
}

// Helpers for opening modals with dynamically populated dropdowns
function openAddStudentModal() {
  populateSelect('newStudProg', state.data.programs, 'Program_ID', p => `${p.Program_Name} (${p.Degree_Level})`);
  document.getElementById('newStudDate').value = new Date().toISOString().slice(0, 10);
  openModal('addStudentModal');
}

function openAddTeacherModal() {
  populateSelect('newTeachDept', state.data.departments, 'Department_ID', d => d.Department_Name);
  openModal('addTeacherModal');
}

function openAddCourseModal() {
  populateSelect('newCrsDept', state.data.departments, 'Department_ID', d => d.Department_Name);
  openModal('addCourseModal');
}

function openAddOfferingModal() {
  populateSelect('newOffCourse', state.data.courses, 'Course_ID', c => `${c.Course_Code} - ${c.Course_Name}`);
  populateSelect('newOffSemester', state.data.semesters, 'Semester_ID', s => `${s.Semester_Name} ${s.Year}`);
  populateSelect('newOffTeacher', state.data.teachers, 'Teacher_ID', t => `${t.Teacher_Name} (${t.Designation})`);
  populateSelect('newOffRoom', state.data.classrooms, 'Room_ID', r => `${r.Building_Name} ${r.Room_Number} (Cap: ${r.Capacity})`);
  openModal('addOfferingModal');
}

function openAddEnrollmentModal() {
  populateSelect('newEnStudent', state.data.students, 'Student_ID', s => `${s.Student_Name} (${s.Registration_No})`);
  populateSelect('newEnOffering', state.data.offerings, 'Offering_ID', o => `${o.Course_Code} - ${o.Course_Name} (Sec ${o.Section}, Prof: ${o.Teacher_Name})`);
  openModal('addEnrollmentModal');
}

function openAddExamModal() {
  populateSelect('newExamOffering', state.data.offerings, 'Offering_ID', o => `${o.Course_Code} - ${o.Course_Name} (Sec ${o.Section})`);
  document.getElementById('newExamDate').value = new Date().toISOString().slice(0, 10);
  openModal('addExamModal');
}

function openMarkAttendanceModal() {
  populateSelect('attOfferingSelect', state.data.offerings, 'Offering_ID', o => `${o.Course_Code} - ${o.Course_Name}`);
  populateSelect('attStudentSelect', state.data.students, 'Student_ID', s => `${s.Student_Name} (${s.Registration_No})`);
  document.getElementById('attDate').value = new Date().toISOString().slice(0, 10);
  openModal('markAttendanceModal');
}

function openAddTimetableModal() {
  populateSelect('ttOfferingSelect', state.data.offerings, 'Offering_ID', o => `${o.Course_Code} - ${o.Course_Name} (Sec ${o.Section})`);
  populateSelect('ttRoomSelect', state.data.classrooms, 'Room_ID', r => `${r.Building_Name} - ${r.Room_Number}`);
  openModal('addTimetableModal');
}

function populateSelect(selectId, items, valKey, textFn) {
  const el = document.getElementById(selectId);
  if (!el) return;
  el.innerHTML = items.map(item => `
    <option value="${item[valKey]}">${escapeHtml(textFn(item))}</option>
  `).join('');
}

// Utilities
function setElementText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text).replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[m]);
}

function showToast(msg, type = 'info') {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed; bottom: 24px; right: 24px; z-index: 9999;
    padding: 12px 20px; border-radius: 8px; font-size: 13.5px; font-weight: 600;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4); animation: fadeIn 0.2s ease;
    background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#4f46e5'};
    color: white;
  `;
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

function showLoader(visible) {
  let loader = document.getElementById('globalLoader');
  if (!loader && visible) {
    loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 3px;
      background: linear-gradient(90deg, #4f46e5, #06b6d4, #8b5cf6);
      z-index: 10000; animation: shimmer 1.5s infinite linear;
    `;
    document.body.appendChild(loader);
  } else if (loader && !visible) {
    loader.remove();
  }
}

// ============================================================================
// INTERACTIVE SQL RUNNER (3NF SCHEMA INSPECTION)
// ============================================================================
function setPresetQuery(id) {
  const input = document.getElementById('sqlConsoleInput');
  if (!input) return;
  if (id === 1) {
    input.value = `SELECT t.Day, t.Start_Time || ' - ' || t.End_Time AS Schedule, c.Course_Code, c.Course_Name, tch.Teacher_Name, cr.Room_Number 
FROM Timetable t 
JOIN Course_Offering co ON t.Offering_ID = co.Offering_ID 
JOIN Course c ON co.Course_ID = c.Course_ID 
JOIN Teacher tch ON co.Teacher_ID = tch.Teacher_ID 
JOIN Classroom cr ON t.Room_ID = cr.Room_ID 
ORDER BY CASE t.Day WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3 WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 ELSE 6 END, t.Start_Time ASC;`;
  } else if (id === 2) {
    input.value = `SELECT s.Registration_No, s.Student_Name, c.Course_Code, e.Exam_Type, r.Obtained_Marks, e.Total_Marks, r.Grade, r.Grade_Point 
FROM Result r 
JOIN Student s ON r.Student_ID = s.Student_ID 
JOIN Exam e ON r.Exam_ID = e.Exam_ID 
JOIN Course_Offering co ON e.Offering_ID = co.Offering_ID 
JOIN Course c ON co.Course_ID = c.Course_ID 
ORDER BY r.Grade_Point DESC;`;
  } else if (id === 3) {
    input.value = `SELECT cr.Building_Name, cr.Room_Number, cr.Capacity, COUNT(t.Timetable_ID) AS Assigned_Classes 
FROM Classroom cr 
LEFT JOIN Timetable t ON cr.Room_ID = t.Room_ID 
GROUP BY cr.Room_ID 
ORDER BY cr.Capacity DESC;`;
  }
  runCustomSql();
}

async function runCustomSql() {
  const input = document.getElementById('sqlConsoleInput');
  const container = document.getElementById('sqlQueryResultContainer');
  const statusEl = document.getElementById('sqlQueryStatus');
  const tableWrapper = document.getElementById('sqlQueryTableWrapper');
  if (!input || !container) return;

  const query = input.value.trim();
  if (!query) {
    showToast('Please enter a SQL query', 'error');
    return;
  }

  container.style.display = 'block';
  statusEl.textContent = 'Executing query...';
  tableWrapper.innerHTML = '';

  try {
    const res = await fetch('/api/execute-sql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Query execution error');

    statusEl.innerHTML = `✅ Query executed successfully &bull; <span style="color:var(--text-main); font-weight:600;">${data.count} rows returned</span>`;

    if (data.rows && data.rows.length > 0) {
      const cols = data.columns;
      tableWrapper.innerHTML = `
        <table>
          <thead>
            <tr>${cols.map(c => `<th>${escapeHtml(c)}</th>`).join('')}</tr>
          </thead>
          <tbody>
            ${data.rows.map(r => `
              <tr>${cols.map(c => `<td>${escapeHtml(String(r[c] !== null ? r[c] : 'NULL'))}</td>`).join('')}</tr>
            `).join('')}
          </tbody>
        </table>
      `;
    } else {
      tableWrapper.innerHTML = '<div style="padding:14px; color:var(--text-muted); text-align:center;">Query returned 0 rows.</div>';
    }
  } catch (err) {
    statusEl.innerHTML = `❌ Error: <span style="color:var(--danger); font-weight:600;">${escapeHtml(err.message)}</span>`;
    tableWrapper.innerHTML = '';
  }
}
