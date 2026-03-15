# 🏫 GraamShala — Rural School Management System
**Hackathon Project | Django | SQLite**

---

## 🚀 Setup in 4 Steps

### Step 1 — Install Django
```bash
pip install django
```

### Step 2 — Run Migrations
```bash
cd rural_school
python manage.py makemigrations core
python manage.py migrate
```

### Step 3 — Load Demo Data
```bash
python manage.py shell < seed_data.py
```

### Step 4 — Create Admin & Run Server
```bash
python manage.py createsuperuser
python manage.py runserver
```

Open: **http://127.0.0.1:8000**
Admin: **http://127.0.0.1:8000/admin**

---

## 📁 Project Structure

```
rural_school/
├── manage.py
├── seed_data.py              ← Demo data loader
├── school_mgmt/
│   ├── settings.py
│   └── urls.py
├── core/
│   ├── models.py             ← Teacher, Student, Attendance, Timetable
│   ├── views.py              ← All page logic
│   ├── urls.py               ← URL routing
│   ├── admin.py              ← Django admin config
│   ├── templatetags/
│   │   └── dict_extras.py    ← Custom template filter
│   └── templates/core/
│       ├── dashboard.html
│       ├── teachers.html
│       ├── teacher_form.html
│       ├── teacher_attendance.html
│       ├── attendance_history.html
│       ├── students.html
│       ├── student_form.html
│       ├── student_attendance.html
│       ├── timetable.html
│       └── mdm_report.html
└── templates/
    └── base.html             ← Sidebar layout, shared UI
```

---

## ✅ Features Implemented

| Module | Feature |
|--------|---------|
| **Dashboard** | Stats overview, quick actions, unmarked teachers alert, class strength chart |
| **Teacher Attendance** | Mark Present/Absent/Late/Leave with remarks, daily records |
| **Student Attendance** | Class & section-wise marking, daily records |
| **Teacher Records** | Add/view teachers with subject, qualification, ID |
| **Student Enrollment** | Full form with class, guardian, Aadhar, category (SC/ST/OBC) |
| **Timetable** | Class-wise, section-wise grid with modal to add periods |
| **MDM Report** | Mid-Day Meal linked to attendance, date-wise government report |
| **Offline Banner** | Auto-detects offline status and shows sync warning |
| **Admin Panel** | Full Django admin for all models |

---

## 🌾 Rural-Specific Features

- **Hindi school name** (GraamShala / Graam Vidyalay Pranali)
- **Category tracking** — General, OBC, SC, ST for government records
- **Aadhar number** field for students
- **MDM (Mid-Day Meal) Report** auto-generated from attendance — submit to BEO
- **Multi-grade classroom support** — Class 1 to 8 with sections
- **Offline detection** banner for areas with poor connectivity
- **Low-bandwidth friendly** — no heavy JS frameworks, pure Django templates
- **IST timezone** — Asia/Kolkata set by default

---

## 🎯 Hackathon Presentation Flow

1. Show **Dashboard** → overview stats, today's unmarked teachers
2. Demo **Teacher Attendance** → mark a few, show instant save
3. Demo **Student Enrollment** → add a new student with Aadhar
4. Show **Student Attendance** → class-wise marking
5. Show **Timetable** → Class 1A grid, add a period via modal
6. Show **MDM Report** → explain government compliance use case
7. Show **Admin Panel** → show all data is stored in SQLite

---

## 📦 Requirements

```
Django>=4.2
```
*(Only standard library + Django — no extra packages needed)*
