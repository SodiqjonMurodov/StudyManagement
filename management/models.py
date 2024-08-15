from django.db import models
from django.contrib.auth.models import User
from accounts.models import *

ATTENDANCE_CONDITION_CHOICES = {
    "": "",
    "1": "Ha",
    "2": "Yo'q"
}

GROUPMEMBER_PERMISSION_CHOICES = {
    "0": "",
    "1": "Aktiv",
    "2": "Taqiqlangan"
}

DAYS_CHOICES = {
    "DU": "Dushanba",
    "SE": "Seshanba",
    "CHOR": "Chorshanba",
    "PAY": "Payshanba",
    "JU": "Juma",
    "SHAN": "Shanba",
    "YAK": "Yakshanba"
}


class Feedback(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id}'


class CompanyInfo(models.Model):
    name = models.CharField(max_length=70)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=255)
    start_day = models.CharField(max_length=4, choices=DAYS_CHOICES, blank=True, null=True)
    end_day = models.CharField(max_length=4, choices=DAYS_CHOICES, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class CourseGroup(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    lang = models.CharField(max_length=30, default="O'zbek")
    start_period = models.DateField()
    end_period = models.DateField()
    students = models.IntegerField()
    study_days = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class GroupContent(models.Model):
    group_id = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.CharField(max_length=150)
    description = models.TextField()
    file = models.FileField(upload_to='files')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.group_id} - {self.topic}'


class GroupMember(models.Model):
    group_id = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1, choices=GROUPMEMBER_PERMISSION_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student_id} - {self.group_id}'


class Payment(models.Model):
    group_member_id = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.group_member_id}'


class Attendance(models.Model):
    group_id = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    group_member_id = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    date = models.DateField()
    condition = models.CharField(max_length=3, choices=ATTENDANCE_CONDITION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'{self.group_member_id} - {self.date}'
