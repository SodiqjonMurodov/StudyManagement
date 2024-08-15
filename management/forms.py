from django import forms
from .models import *
from accounts.models import *


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mavzu'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '6', 'placeholder': 'Xabar'}),
        }


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'image', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kurs nomi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Kurs tavsifi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kurs narxi'}),
        }


class GroupAddForm(forms.ModelForm):
    course_id = forms.ModelChoiceField(queryset=Course.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control select-arrow'}))
    mentor_id = forms.ModelChoiceField(queryset=Profile.objects.filter(role=2),
                                       widget=forms.Select(attrs={'class': 'form-control select-arrow'}))

    class Meta:
        model = CourseGroup
        fields = ['course_id', 'mentor_id', 'name', 'start_period', 'end_period', 'students', 'study_days', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guruh nomi'}),
            'start_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'end_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'students': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Studentlar soni'}),
            'study_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "O'qish kunlari"}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
        }


class CompanyEditForm(forms.ModelForm):
    start_day = forms.ChoiceField(choices = DAYS_CHOICES,
                                  widget=forms.Select(attrs={'class':'form-select w-auto py-1'})) 
    end_day = forms.ChoiceField(choices = DAYS_CHOICES,
                                  widget=forms.Select(attrs={'class':'form-select w-auto py-1'})) 

    class Meta:
        model = CompanyInfo
        fields = ['name', 'address', 'phone', 'email', 'start_day', 'end_day', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guruh nomi'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Studentlar soni'}),
            'start_time': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Studentlar soni', 'type': 'time'}),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Studentlar soni', 'type': 'time'})
        }


class GroupContentAddForm(forms.ModelForm):
    group_id = forms.ModelChoiceField(queryset=GroupContent.objects.filter(),
                                       widget=forms.Select(attrs={'class': 'form-control select-arrow'}))

    class Meta:
        model = GroupContent
        fields = ['group_id', 'topic', 'description', 'file']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mavzu nomi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Mavzu tavsifi'})
        }


class GroupContentEditForm(forms.ModelForm):

    class Meta:
        model = GroupContent
        fields = ['topic', 'description', 'file']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mavzu nomi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Mavzu tavsifi'})
        }


class AttendanceForm(forms.ModelForm):
    condition = forms.ChoiceField(choices = ATTENDANCE_CONDITION_CHOICES, required=False, 
                                  widget=forms.Select(attrs={'class':'form-select w-auto py-1'})) 

    class Meta:
        model = Attendance
        fields = ['condition']


class AttendanceEditForm(forms.ModelForm):
    condition = forms.ChoiceField(choices = ATTENDANCE_CONDITION_CHOICES, required=False, 
                                  widget=forms.Select(attrs={'class':'form-select w-auto py-1'}))
    group_id = forms.ModelChoiceField(queryset=CourseGroup.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control select-arrow'}))
    group_member_id = forms.ModelChoiceField(queryset=GroupMember.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control select-arrow'}))

    class Meta:
        model = Attendance
        fields = ['condition', 'group_id', 'group_member_id', 'date']
        widgets ={
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d')
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Izoh qoldirish uchun joy'})
        }


class PermissionEditForm(forms.ModelForm):
    permission = forms.ChoiceField(choices = GROUPMEMBER_PERMISSION_CHOICES, required=False,
                                  widget=forms.Select(attrs={'class':'form-select w-auto py-1'}))

    class Meta:
        model = GroupMember
        fields = ['permission']