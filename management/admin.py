from django.contrib import admin
from .models import *
from accounts.models import Profile

admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(CompanyInfo)
admin.site.register(Course)
admin.site.register(CourseGroup)
admin.site.register(Attendance)
admin.site.register(GroupMember)
admin.site.register(GroupContent)
admin.site.register(Payment)