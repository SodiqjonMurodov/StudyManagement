from django.db import models
from django.contrib.auth.models import User, Group
    
ATTENDANCE_GENDER_CHOICES = {
        "": "",
        "1": "Erkak",
        "2": "Ayol"
    }


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.ForeignKey(Group, on_delete=models.PROTECT, default=1)
    email = models.EmailField(max_length=255)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=5, choices=ATTENDANCE_GENDER_CHOICES)
    phone = models.CharField(max_length=14)
    about = models.TextField(blank=True, null=True)
    facebook_link = models.CharField(max_length=255, blank=True, null=True)
    telegram_link = models.CharField(max_length=255, blank=True, null=True)
    instagram_link = models.CharField(max_length=255, blank=True, null=True)
    twitter_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
