from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile-init", profile_init, name="profile-init"),
    path("profile/<int:pk>/", ProfileUpdateView.as_view(), name="profile"),
    path("terms-and-policy", TermAndPolicyView.as_view(), name="terms-and-policy"),
    path('teachers', TeachersPageView.as_view(), name='teachers_page'),
    path('students', StudentsPageView.as_view(), name='students_page'),
    path('teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('edit-user/<int:pk>', UserUpdateView.as_view(), name='edit-user'),
]
