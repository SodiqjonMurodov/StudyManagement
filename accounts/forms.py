from django import forms
from django.contrib.auth.models import User, Group
from .models import *


class ProfileInitForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=ATTENDANCE_GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'birthday', 'gender', 'phone']
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }


class ProfileEditForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=ATTENDANCE_GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'birthday', 'gender', 'phone', 'about',
                  'facebook_link', 'telegram_link', 'instagram_link', 'twitter_link', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_link': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserEditForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=ATTENDANCE_GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-select'}))
    role = forms.ModelChoiceField(queryset=Group.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control select-arrow'}))

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name', 'role', 'email', 'birthday', 'gender', 'phone', 'about',
                  'facebook_link', 'telegram_link', 'instagram_link', 'twitter_link']
        widgets = {
            'user_id': forms.NumberInput(attrs={'type': 'hidden'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_link': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control'}),
        }
