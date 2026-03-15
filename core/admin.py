from django.contrib import admin
from .models import Teacher, Student, TeacherAttendance, StudentAttendance, Timetable, Announcement

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_id', 'subject', 'phone', 'joining_date', 'is_active']
    list_filter = ['subject', 'is_active']
    search_fields = ['name', 'employee_id', 'phone']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'student_class', 'section', 'guardian_name', 'guardian_phone', 'category']
    list_filter = ['student_class', 'section', 'category']
    search_fields = ['name', 'roll_number', 'guardian_name']

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'date', 'status', 'remarks']
    list_filter = ['status', 'date']
    date_hierarchy = 'date'

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status']
    list_filter = ['status', 'date']
    date_hierarchy = 'date'

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['student_class', 'section', 'day', 'period', 'subject', 'teacher']
    list_filter = ['student_class', 'day']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'target', 'created_at']
