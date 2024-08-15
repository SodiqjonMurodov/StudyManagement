from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from .models import *
from management.models import CompanyInfo
from django.contrib.auth.models import User
from .forms import *
from management.views import GetData


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('profile-init')

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid


class TermAndPolicyView(TemplateView):
    template_name = 'registration/terms-and-policy.html'


@login_required
def profile_init(request):
    if request.method == "POST":
        profile_form = ProfileInitForm(request.POST)
        if profile_form.is_valid():
            # Create profile
            profile_data = Profile(
                user_id=request.user,
                birthday=profile_form.cleaned_data['birthday'],
                gender=profile_form.cleaned_data['gender'],
                phone=profile_form.cleaned_data['phone'],
                first_name=profile_form.cleaned_data['first_name'],
                last_name=profile_form.cleaned_data['last_name'],
                email=profile_form.cleaned_data['email'],
            )
            profile_data.save()

            # Add in Student group
            user = User.objects.get(pk=request.user.id)
            student = Group.objects.get(name='Student')
            user.groups.add(student)

            return redirect('home_page')
        else:
            print('--form invalid--')

    else:
        profile_form = ProfileInitForm()
    return render(request, 'registration/profile-init.html',
                  context={'profile_form': profile_form})


class ProfileUpdateView(LoginRequiredMixin, GetData, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    success_url = reverse_lazy('home_page')
    template_name = 'accounts/profile.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        else:
            print("--form invalid--")
        return super().form_valid(form)



class TeachersPageView(LoginRequiredMixin, GetData, TemplateView):
    template_name = 'accounts/teachers.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeachersPageView, self).get_context_data(*args, **kwargs)
        mentor = Group.objects.get(name='Mentor')
        context['users'] = Profile.objects.filter(role=mentor)
        return context


class StudentsPageView(LoginRequiredMixin, GetData, TemplateView):
    template_name = 'accounts/students.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentsPageView, self).get_context_data(*args, **kwargs)
        student = Group.objects.get(name='Student')
        context['users'] = Profile.objects.filter(role=student)
        return context


class UserUpdateView(LoginRequiredMixin, GetData, UpdateView):
    model = Profile
    form_class = UserEditForm
    success_url = reverse_lazy('home_page')
    template_name = 'accounts/user-edit.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            role = form.cleaned_data['role'].id
            user_id = form.cleaned_data['user_id'].id
            user = User.objects.get(pk=user_id)
            role1 = Group.objects.get(name='Student')
            role2 = Group.objects.get(name='Mentor')
            role3 = Group.objects.get(name='Admin')
            if role == 1:
                user.groups.clear()
                user.groups.add(role1)
            elif role == 2:
                user.groups.clear()
                user.groups.add(role2)
            elif role == 3:
                user.groups.clear()
                user.groups.add(role3)
        else:
            print("--form invalid--")
        return super().form_valid(form)


class TeacherDeleteView(LoginRequiredMixin, GetData, DeleteView):
    model = User
    success_url = reverse_lazy('teachers_page')
    template_name = 'accounts/user-delete.html'


class StudentDeleteView(LoginRequiredMixin, GetData, DeleteView):
    model = User
    success_url = reverse_lazy('students_page')
    template_name = 'accounts/user-delete.html'
