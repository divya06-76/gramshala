from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import (Teacher, Student, TeacherAttendance, StudentAttendance,
                     Timetable, Announcement)
import json


def dashboard(request):
    today = timezone.now().date()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_students = Student.objects.filter(is_active=True).count()

    teachers_present = TeacherAttendance.objects.filter(
        date=today, status='Present').count()
    teachers_absent = TeacherAttendance.objects.filter(
        date=today, status='Absent').count()
    students_present = StudentAttendance.objects.filter(
        date=today, status='Present').count()

    # Class-wise student count
    class_data = Student.objects.filter(is_active=True).values(
        'student_class').annotate(count=Count('id')).order_by('student_class')

    recent_announcements = Announcement.objects.all()[:3]
    unmarked_teachers = Teacher.objects.filter(is_active=True).exclude(
        teacher_attendance__date=today
    )

    context = {
        'total_teachers': total_teachers,
        'total_students': total_students,
        'teachers_present': teachers_present,
        'teachers_absent': teachers_absent,
        'students_present': students_present,
        'class_data': list(class_data),
        'recent_announcements': recent_announcements,
        'unmarked_teachers': unmarked_teachers,
        'today': today,
    }
    return render(request, 'core/dashboard.html', context)


# ─── TEACHERS ───────────────────────────────────────────────
def teacher_list(request):
    teachers = Teacher.objects.filter(is_active=True).order_by('name')
    today = timezone.now().date()
    return render(request, 'core/teachers.html', {'teachers': teachers, 'today': today})


def teacher_add(request):
    if request.method == 'POST':
        try:
            Teacher.objects.create(
                name=request.POST['name'],
                employee_id=request.POST['employee_id'],
                phone=request.POST['phone'],
                subject=request.POST['subject'],
                qualification=request.POST.get('qualification', 'B.Ed'),
                joining_date=request.POST['joining_date'],
            )
            messages.success(request, f"Teacher {request.POST['name']} added successfully!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
        return redirect('teachers')
    return render(request, 'core/teacher_form.html')


def teacher_attendance(request):
    today = timezone.now().date()
    teachers = Teacher.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        for teacher in teachers:
            status = request.POST.get(f'status_{teacher.id}', 'Present')
            remarks = request.POST.get(f'remarks_{teacher.id}', '')
            TeacherAttendance.objects.update_or_create(
                teacher=teacher, date=today,
                defaults={'status': status, 'remarks': remarks}
            )
        messages.success(request, "Teacher attendance saved successfully!")
        return redirect('teacher_attendance')

    attendance_map = {}
    for a in TeacherAttendance.objects.filter(date=today):
        attendance_map[a.teacher_id] = a

    return render(request, 'core/teacher_attendance.html', {
        'teachers': teachers,
        'attendance_map': attendance_map,
        'today': today,
    })


def teacher_attendance_history(request):
    records = TeacherAttendance.objects.select_related('teacher').order_by('-date')[:100]
    return render(request, 'core/attendance_history.html', {'records': records, 'type': 'teacher'})


# ─── STUDENTS ───────────────────────────────────────────────
def student_list(request):
    cls = request.GET.get('class', '')
    students = Student.objects.filter(is_active=True)
    if cls:
        students = students.filter(student_class=cls)
    students = students.order_by('student_class', 'roll_number')
    classes = [str(i) for i in range(1, 9)]
    return render(request, 'core/students.html', {
        'students': students, 'classes': classes, 'selected_class': cls
    })


def student_add(request):
    if request.method == 'POST':
        try:
            Student.objects.create(
                name=request.POST['name'],
                roll_number=request.POST['roll_number'],
                student_class=request.POST['student_class'],
                section=request.POST.get('section', 'A'),
                guardian_name=request.POST['guardian_name'],
                guardian_phone=request.POST['guardian_phone'],
                address=request.POST['address'],
                date_of_birth=request.POST['date_of_birth'],
                aadhar_number=request.POST.get('aadhar_number', ''),
                category=request.POST.get('category', 'General'),
            )
            messages.success(request, f"Student {request.POST['name']} enrolled successfully!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
        return redirect('students')
    return render(request, 'core/student_form.html')


def student_attendance(request):
    today = timezone.now().date()
    cls = request.GET.get('class', '1')
    section = request.GET.get('section', 'A')
    students = Student.objects.filter(is_active=True, student_class=cls, section=section)

    if request.method == 'POST':
        cls = request.POST.get('class', '1')
        section = request.POST.get('section', 'A')
        students = Student.objects.filter(is_active=True, student_class=cls, section=section)
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'Absent')
            StudentAttendance.objects.update_or_create(
                student=student, date=today,
                defaults={'status': status}
            )
        messages.success(request, f"Attendance for Class {cls}{section} saved!")
        return redirect(f'/students/attendance/?class={cls}&section={section}')

    attendance_map = {}
    for a in StudentAttendance.objects.filter(date=today, student__student_class=cls, student__section=section):
        attendance_map[a.student_id] = a

    classes = [str(i) for i in range(1, 9)]
    return render(request, 'core/student_attendance.html', {
        'students': students, 'attendance_map': attendance_map,
        'today': today, 'cls': cls, 'section': section, 'classes': classes,
    })


# ─── TIMETABLE ──────────────────────────────────────────────
def timetable_view(request):
    cls = request.GET.get('class', '1')
    section = request.GET.get('section', 'A')
    entries = Timetable.objects.filter(
        student_class=cls, section=section
    ).select_related('teacher').order_by('period')

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    periods = [str(i) for i in range(1, 8)]

    grid = {day: {p: None for p in periods} for day in days}
    for e in entries:
        grid[e.day][e.period] = e

    classes = [str(i) for i in range(1, 9)]
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'core/timetable.html', {
        'grid': grid, 'days': days, 'periods': periods,
        'cls': cls, 'section': section, 'classes': classes, 'teachers': teachers,
    })


def timetable_add(request):
    if request.method == 'POST':
        try:
            teacher_id = request.POST.get('teacher')
            teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
            Timetable.objects.update_or_create(
                student_class=request.POST['student_class'],
                section=request.POST.get('section', 'A'),
                day=request.POST['day'],
                period=request.POST['period'],
                defaults={
                    'subject': request.POST['subject'],
                    'teacher': teacher,
                    'start_time': request.POST['start_time'],
                    'end_time': request.POST['end_time'],
                }
            )
            messages.success(request, "Timetable entry saved!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
        cls = request.POST.get('student_class', '1')
        sec = request.POST.get('section', 'A')
        return redirect(f'/timetable/?class={cls}&section={sec}')


# ─── REPORTS ────────────────────────────────────────────────
def mdm_report(request):
    """Mid-Day Meal Report - attendance-linked daily report"""
    today = timezone.now().date()
    report_date = request.GET.get('date', str(today))

    class_report = []
    for i in range(1, 9):
        students = Student.objects.filter(is_active=True, student_class=str(i))
        total = students.count()
        present = StudentAttendance.objects.filter(
            date=report_date, status='Present',
            student__student_class=str(i)
        ).count()
        class_report.append({
            'class': i, 'total': total,
            'present': present, 'absent': total - present,
            'mdm_beneficiaries': present,
        })

    grand_total = sum(r['total'] for r in class_report)
    grand_present = sum(r['present'] for r in class_report)

    return render(request, 'core/mdm_report.html', {
        'class_report': class_report,
        'grand_total': grand_total,
        'grand_present': grand_present,
        'report_date': report_date,
    })

def landing(request):
    return render(request, 'core/landing.html')