from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('contact', ContactPageView.as_view(), name='contact'),
    path('contact-edit/<int:pk>', CompanyEditView.as_view(), name='contact-edit'),
    path('permissions', PermissionsPageView.as_view(), name='permissions'),
    path('permission/add/<int:group_id>', permission_add, name='permission_add'),
    path('download-check/<int:check_id>', download_check, name='download_check'),
    path('permission/edit/<int:pk>', PermissionEditView.as_view(), name='permission_edit'),
    path('messages', MessagesPageView.as_view(), name='messages'),
    path('pages_404', Error404PageView.as_view(), name='error-404'),
    path('pages_500', Error500PageView.as_view(), name='error-500'),
    # Courses
    path('courses/all', CoursesPageView.as_view(), name='courses_page'),
    path('course/edit/<pk>/', CourseEditView.as_view(), name='course_edit'),
    path('course/delete/<pk>/', CourseDeleteView.as_view(), name='course_delete'),
    path('courses', CoursesStudentPageView.as_view(), name='courses_student'),
    path('mycourses', MyCoursesPageView.as_view(), name='my_courses'),
    path('course-details/<pk>/', CourseDetailsView.as_view(), name='course_details'),
    path('download-file/<int:file_id>/', download_file, name='download_file'),
    path('course-add', CourseAddView.as_view(), name='course-add'),
    path('filter/', FilterGroupsView.as_view(), name='filter'),
    # Groups
    path('groups', GroupsPageView.as_view(), name='groups'),
    path('groups/student/<pk>', GroupsPageStudentView.as_view(), name='groups_student'),
    path('groups/mentor', GroupsPageMentorView.as_view(), name='groups_mentor'),
    path('group', CourseDetailsView.as_view(), name='course_details'),
    path('groups/group-add', GroupAddView.as_view(), name='group-add'),
    path('groups/group-edit/<int:pk>', GroupEditView.as_view(), name='group-edit'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('group-content/<int:gr>/add/', GroupContentAddView.as_view(), name='group_content_add'),
    path('group-content/<int:pk>/edit/', GroupContentEditView.as_view(), name='group_content_edit'),
    path('group-content/<int:pk>/delete/', GroupContentDeleteView.as_view(), name='group_content_delete'),
    # Attendance
    path('attendance/admin/', AttendanceAdminPageView.as_view(), name='attendance_admin'),
    path('attendance/edit/<pk>', AttendanceEditView.as_view(), name='attendance_edit'),
    path('attendance/delete/<pk>', AttendanceDeleteView.as_view(), name='attendance_delete'),
    path('attendance/student/', AttendanceStudentPageView.as_view(), name='attendance_student'),
    path('attendance/mentor/', AttendanceMentorPageView.as_view(), name='attendance_mentor'),
    path('filter/attendance/mentor/', FilterAttendanceMentorPageView.as_view(), name='filter_attendance_mentor')
]