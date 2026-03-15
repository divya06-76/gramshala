from django.db import models
from django.utils import timezone

CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(1, 9)]
SECTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]
DAY_CHOICES = [
    ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'),
]
PERIOD_CHOICES = [(str(i), f'Period {i}') for i in range(1, 8)]

SUBJECT_CHOICES = [
    ('Hindi', 'Hindi'), ('English', 'English'), ('Math', 'Mathematics'),
    ('Science', 'Science'), ('Social', 'Social Studies'), ('Computer', 'Computer'),
    ('Art', 'Art & Craft'), ('PT', 'Physical Education'),
]


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    qualification = models.CharField(max_length=100, default='B.Ed')
    joining_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.subject})"

    def attendance_today(self):
        today = timezone.now().date()
        record = self.teacher_attendance.filter(date=today).first()
        if record:
            return record.status
        return 'Not Marked'


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=5, choices=CLASS_CHOICES)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES, default='A')
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    admission_date = models.DateField(default=timezone.now)
    aadhar_number = models.CharField(max_length=12, blank=True)
    category = models.CharField(max_length=20, choices=[
        ('General', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')
    ], default='General')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - Class {self.student_class}{self.section}"

    def attendance_today(self):
        today = timezone.now().date()
        record = self.student_attendance.filter(date=today).first()
        if record:
            return record.status
        return 'Not Marked'

    class Meta:
        ordering = ['student_class', 'roll_number']


class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late'), ('Leave', 'On Leave')
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_attendance')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    remarks = models.CharField(max_length=200, blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['teacher', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.teacher.name} - {self.date} - {self.status}"


class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']


class Timetable(models.Model):
    student_class = models.CharField(max_length=5, choices=CLASS_CHOICES)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES, default='A')
    day = models.CharField(max_length=5, choices=DAY_CHOICES)
    period = models.CharField(max_length=2, choices=PERIOD_CHOICES)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ['student_class', 'section', 'day', 'period']
        ordering = ['day', 'period']

    def __str__(self):
        return f"Class {self.student_class}{self.section} - {self.day} P{self.period} - {self.subject}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    target = models.CharField(max_length=20, choices=[
        ('All', 'Everyone'), ('Teachers', 'Teachers Only'), ('Parents', 'Parents Only')
    ], default='All')

    class Meta:
        ordering = ['-created_at']
