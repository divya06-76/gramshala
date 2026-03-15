from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Teachers
    path('teachers/', views.teacher_list, name='teachers'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),
    path('teachers/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('teachers/attendance/history/', views.teacher_attendance_history, name='teacher_attendance_history'),

    # Students
    path('students/', views.student_list, name='students'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/attendance/', views.student_attendance, name='student_attendance'),

    # Timetable
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.timetable_add, name='timetable_add'),

    # Reports
    path('reports/mdm/', views.mdm_report, name='mdm_report'),
]
