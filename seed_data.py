"""
Run this to load demo data for the hackathon:
    python manage.py shell < seed_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_mgmt.settings')
django.setup()

from django.utils import timezone
from core.models import Teacher, Student, TeacherAttendance, StudentAttendance, Timetable, Announcement

print("🌱 Seeding demo data...")

# ── Teachers ──────────────────────────────────────────────
teachers_data = [
    ("Ramesh Kumar Sharma",    "EMP001", "9876543210", "Hindi",    "M.A., B.Ed"),
    ("Sunita Devi Patel",      "EMP002", "9876543211", "Math",     "B.Sc., B.Ed"),
    ("Arvind Singh Rajput",    "EMP003", "9876543212", "Science",  "B.Sc., B.Ed"),
    ("Geeta Kumari Yadav",     "EMP004", "9876543213", "English",  "M.A., B.Ed"),
    ("Mohan Lal Vishwakarma",  "EMP005", "9876543214", "Social",   "B.A., B.Ed"),
    ("Priya Shukla",           "EMP006", "9876543215", "Computer", "BCA, B.Ed"),
]

teachers = []
for name, eid, phone, subj, qual in teachers_data:
    t, _ = Teacher.objects.get_or_create(employee_id=eid, defaults={
        'name': name, 'phone': phone, 'subject': subj,
        'qualification': qual, 'joining_date': '2022-06-15'
    })
    teachers.append(t)
print(f"  ✅ {len(teachers)} teachers created")

# ── Students ──────────────────────────────────────────────
students_data = [
    ("Anjali Kumari",    "2024-001", "1", "A", "Rajendra Prasad",   "9111111101", "Piparia, Seoni", "2014-04-10", "General"),
    ("Rohit Yadav",      "2024-002", "1", "A", "Suresh Yadav",      "9111111102", "Dhuma, Seoni",   "2014-07-22", "OBC"),
    ("Kavya Singh",      "2024-003", "2", "A", "Virendra Singh",    "9111111103", "Barghat, Seoni", "2013-03-15", "General"),
    ("Rahul Patel",      "2024-004", "2", "A", "Dinesh Patel",      "9111111104", "Lakhnadon",      "2013-11-05", "OBC"),
    ("Pooja Ahirwar",    "2024-005", "3", "A", "Ramswaroop Ahirwar","9111111105", "Chhapara",       "2012-08-20", "SC"),
    ("Deepak Lodhi",     "2024-006", "3", "A", "Bhagwandas Lodhi",  "9111111106", "Keolari, Seoni", "2012-01-30", "OBC"),
    ("Sakshi Jain",      "2024-007", "4", "A", "Mahesh Jain",       "9111111107", "Seoni City",     "2011-06-14", "General"),
    ("Aditya Kori",      "2024-008", "4", "A", "Ramkhelawan Kori",  "9111111108", "Barghat",        "2011-09-25", "SC"),
    ("Nisha Prajapati",  "2024-009", "5", "A", "Tilak Prajapati",   "9111111109", "Ghansore",       "2010-02-18", "OBC"),
    ("Saurabh Tiwari",   "2024-010", "5", "A", "Kamlesh Tiwari",    "9111111110", "Dhooma, Seoni",  "2010-12-07", "General"),
    ("Ritu Gond",        "2024-011", "6", "A", "Budhelal Gond",     "9111111111", "Kurai, Seoni",   "2009-05-11", "ST"),
    ("Vikram Sahu",      "2024-012", "6", "A", "Badrilal Sahu",     "9111111112", "Munger, Seoni",  "2009-08-30", "OBC"),
    ("Prachi Mishra",    "2024-013", "7", "A", "Shivkumar Mishra",  "9111111113", "Seoni",          "2008-03-22", "General"),
    ("Lokesh Dhurve",    "2024-014", "7", "A", "Jagdish Dhurve",    "9111111114", "Chhapara",       "2008-10-14", "ST"),
    ("Ankita Pal",       "2024-015", "8", "A", "Santosh Pal",       "9111111115", "Seoni",          "2007-07-05", "OBC"),
    ("Shubham Namdev",   "2024-016", "8", "A", "Ramkumar Namdev",   "9111111116", "Lakhnadon",      "2007-11-19", "OBC"),
]

students = []
for row in students_data:
    name, roll, cls, sec, gname, gphone, addr, dob, cat = row
    s, _ = Student.objects.get_or_create(roll_number=roll, defaults={
        'name': name, 'student_class': cls, 'section': sec,
        'guardian_name': gname, 'guardian_phone': gphone,
        'address': addr, 'date_of_birth': dob, 'category': cat
    })
    students.append(s)
print(f"  ✅ {len(students)} students created")

# ── Today's Teacher Attendance ─────────────────────────────
import random
today = timezone.now().date()
statuses = ['Present', 'Present', 'Present', 'Present', 'Late', 'Absent']
for t in teachers:
    TeacherAttendance.objects.get_or_create(teacher=t, date=today, defaults={
        'status': random.choice(statuses)
    })
print(f"  ✅ Teacher attendance for {today} added")

# ── Today's Student Attendance ─────────────────────────────
for s in students:
    st = random.choice(['Present', 'Present', 'Present', 'Absent'])
    StudentAttendance.objects.get_or_create(student=s, date=today, defaults={'status': st})
print(f"  ✅ Student attendance for {today} added")

# ── Timetable (Class 1A) ───────────────────────────────────
tt_data = [
    ("1","A","Mon","1","Hindi",   teachers[0], "09:00","09:45"),
    ("1","A","Mon","2","Math",    teachers[1], "09:45","10:30"),
    ("1","A","Mon","3","English", teachers[3], "10:45","11:30"),
    ("1","A","Mon","4","Science", teachers[2], "11:30","12:15"),
    ("1","A","Tue","1","Math",    teachers[1], "09:00","09:45"),
    ("1","A","Tue","2","Hindi",   teachers[0], "09:45","10:30"),
    ("1","A","Tue","3","Social",  teachers[4], "10:45","11:30"),
    ("1","A","Tue","4","Computer",teachers[5], "11:30","12:15"),
    ("1","A","Wed","1","English", teachers[3], "09:00","09:45"),
    ("1","A","Wed","2","Science", teachers[2], "09:45","10:30"),
    ("1","A","Wed","3","Hindi",   teachers[0], "10:45","11:30"),
    ("1","A","Wed","4","Math",    teachers[1], "11:30","12:15"),
    ("1","A","Thu","1","Social",  teachers[4], "09:00","09:45"),
    ("1","A","Thu","2","Computer",teachers[5], "09:45","10:30"),
    ("1","A","Thu","3","Math",    teachers[1], "10:45","11:30"),
    ("1","A","Thu","4","Science", teachers[2], "11:30","12:15"),
    ("1","A","Fri","1","Hindi",   teachers[0], "09:00","09:45"),
    ("1","A","Fri","2","English", teachers[3], "09:45","10:30"),
    ("1","A","Fri","3","Social",  teachers[4], "10:45","11:30"),
    ("1","A","Fri","4","PT",      None,         "11:30","12:15"),
    ("1","A","Sat","1","Art",     None,         "09:00","09:45"),
    ("1","A","Sat","2","Hindi",   teachers[0], "09:45","10:30"),
]
for cls, sec, day, period, subj, teacher, st, et in tt_data:
    Timetable.objects.get_or_create(
        student_class=cls, section=sec, day=day, period=period,
        defaults={'subject': subj, 'teacher': teacher, 'start_time': st, 'end_time': et}
    )
print(f"  ✅ Timetable entries created")

# ── Announcements ──────────────────────────────────────────
announcements = [
    ("Parent-Teacher Meeting", "PTM scheduled for Saturday 20th July at 10 AM. All parents are requested to attend.", "All"),
    ("Annual Sports Day", "Annual Sports Day will be held on 15 August. Practice starts from 1 August.", "All"),
    ("Fee Reminder", "Last date for session fee payment is 31 July. Kindly pay on time.", "Parents"),
    ("Staff Meeting", "Mandatory staff meeting on Monday 22nd July at 3 PM in the principal's office.", "Teachers"),
]
for title, msg, target in announcements:
    Announcement.objects.get_or_create(title=title, defaults={'message': msg, 'target': target})
print(f"  ✅ Announcements created")

print("\n🎉 Demo data loaded successfully!")
print("   Run: python manage.py runserver")
print("   Open: http://127.0.0.1:8000")
