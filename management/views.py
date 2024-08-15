from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from accounts.models import Profile
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


class GetData:
    def get_profile(self):
        return Profile.objects.get(user_id=self.request.user.id)
    
    def get_username(self):
        return User.objects.get(pk=self.request.user.id)
    
    def get_company_info(self):
        return CompanyInfo.objects.get(pk=1)
    
    def get_courses(self):
        return Course.objects.all()
    
    def get_today(self):
        return date.today()
    

class HomePageView(LoginRequiredMixin, GetData, TemplateView):
    template_name = 'management/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.count
        context['groups'] = CourseGroup.objects.count
        context['mentors'] = Profile.objects.filter(role=2).count
        context['students'] = Profile.objects.filter(role=1).count

        return context


class CoursesPageView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 8
    model = Course
    template_name = 'management/courses.html'

class CoursesStudentPageView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 8
    model = CourseGroup
    template_name = 'management/courses-student.html'

    def get_queryset(self):
        groups = CourseGroup.objects.filter(start_period__gt=str(date.today()))
        group_id_list = []
        course_list = []
        for i in groups:
            if not str(i.course_id) in course_list:
                group_id_list.append(str(i.id))
                course_list.append(str(i.course_id))
        return CourseGroup.objects.filter(id__in=group_id_list, start_period__gt=date.today())
    

class MyCoursesPageView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 8
    model = GroupMember
    template_name = 'management/mycourses.html'

    def get_queryset(self):
        user_id = Profile.objects.get(user_id=self.request.user.id)
        return GroupMember.objects.filter(student_id=user_id)


class CourseAddView(LoginRequiredMixin, GetData, CreateView):
    form_class = CourseAddForm
    template_name = 'management/course-add.html'
    success_url = 'course-add'


class CourseEditView(LoginRequiredMixin, GetData, UpdateView):
    model = Course
    form_class = CourseAddForm
    success_url = reverse_lazy('courses_page')
    template_name = 'management/course-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_img'] = Course.objects.get(pk=self.kwargs.get('pk'))
        return context
    

class CourseDeleteView(LoginRequiredMixin, GetData, DeleteView):
    model = Course
    success_url = reverse_lazy('courses_page')
    template_name = 'management/course-delete.html'
    

class CourseDetailsView(LoginRequiredMixin, GetData, DetailView, CreateView):
    model = CourseGroup
    template_name = 'management/course-details.html'
    form_class = PaymentForm

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailsView, self).get_context_data(*args, **kwargs)
        group_id = CourseGroup.objects.get(pk=self.kwargs.get('pk'))
        context['content'] = GroupContent.objects.filter(group_id=group_id)
        context['members'] = GroupMember.objects.filter(group_id=group_id, permission="1")
        try:
            member_id = Profile.objects.get(user_id=self.request.user)
            context['group_member'] = GroupMember.objects.get(student_id=member_id, group_id=group_id)
            print(context['group_member'])
            context['student_checks'] = Payment.objects.filter(group_member_id=context['group_member'].id)
        except:
            context['group_member'] = ""
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            group_id = CourseGroup.objects.get(pk=self.kwargs.get('pk'))
            student_id=Profile.objects.get(user_id=self.request.user.id)
            payment_data = Payment(
                group_member_id=GroupMember.objects.get(student_id=student_id, group_id=group_id),
                file=form.cleaned_data['file'],
                description=form.cleaned_data['description']
            )
            payment_data.save()
            return redirect('my_courses')
        else:
            print('--form invalid--')
        return super().form_valid(form)
    

def download_file(request, file_id):
    uploaded_file = GroupContent.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response


class GroupsPageView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 6
    model = CourseGroup
    template_name = 'management/groups.html'


class GroupsPageStudentView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 6
    model = CourseGroup
    template_name = 'management/groups-student.html'

    def get_queryset(self):
        get_group=CourseGroup.objects.get(pk=self.kwargs.get('pk'))
        return CourseGroup.objects.filter(course_id=get_group.course_id, start_period__gt=date.today())


class GroupsPageMentorView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 6
    model = CourseGroup
    template_name = 'management/groups-mentor.html'

    def get_queryset(self):
        profile = Profile.objects.get(user_id=self.request.user.id)
        return CourseGroup.objects.filter(mentor_id=profile)


class FilterGroupsView(GroupsPageView, ListView):
    def get_queryset(self):
        query = self.request.GET.getlist("course_id")
        if query == ['on']:
            queryset = CourseGroup.objects.all()
        else:
            queryset = CourseGroup.objects.filter(course_id__in=self.request.GET.getlist("course_id"))
            if not queryset.exists():
                queryset = CourseGroup.objects.all()
        return queryset


class GroupAddView(LoginRequiredMixin, GetData, CreateView):
    form_class = GroupAddForm
    template_name = 'management/group-add.html'
    success_url = 'group-add'


class GroupEditView(LoginRequiredMixin, GetData, UpdateView):
    model = CourseGroup
    form_class = GroupAddForm
    success_url = reverse_lazy('groups')
    template_name = 'management/group-edit.html'



class GroupDeleteView(LoginRequiredMixin, GetData, DeleteView):
    model = CourseGroup
    success_url = reverse_lazy('groups')
    template_name = 'management/group-delete.html'


class GroupContentAddView(LoginRequiredMixin, GetData, CreateView):
    form_class = GroupContentEditForm
    template_name = 'management/group-content-add.html'
    success_url = 'groups_mentor'

    def form_valid(self, form):
        if form.is_valid():
            content_data = GroupContent(
                group_id=CourseGroup.objects.get(pk=self.kwargs.get('gr')),
                topic=form.cleaned_data['topic'],
                description=form.cleaned_data['description'],
                file=form.cleaned_data['file'],
            )
            content_data.save()
            return redirect('groups_mentor')
        else:
            print('--form invalid--')
        return super().form_valid(form)
    

class GroupContentEditView(LoginRequiredMixin, GetData, UpdateView):
    model = GroupContent
    form_class = GroupContentEditForm
    success_url = reverse_lazy('groups_mentor')
    template_name = 'management/group-content-edit.html'
    

class GroupContentDeleteView(LoginRequiredMixin, GetData, DeleteView):
    model = GroupContent
    success_url = reverse_lazy('groups_mentor')
    template_name = 'management/group-content-delete.html'


class ContactPageView(LoginRequiredMixin, GetData, CreateView):
    form_class = FeedbackForm
    template_name = 'management/contact.html'
    success_url = 'contact'

    def form_valid(self, form):
        if form.is_valid():
            # Create feedback
            feedback_data = Feedback(
                user_id=self.request.user,
                title=form.cleaned_data['title'],
                message=form.cleaned_data['message'],
            )
            feedback_data.save()
            return redirect('contact')
        else:
            print('--form invalid--')
        return super().form_valid(form)


class AttendanceStudentPageView(LoginRequiredMixin, GetData, TemplateView):
    template_name = 'management/attendance-student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = Profile.objects.get(user_id=self.request.user.id)
        student_id = GroupMember.objects.filter(student_id=profile_id.id)
        context['attendance'] = Attendance.objects.filter(group_member_id__in=student_id, condition__in=[1, 2])
        return context


class AttendanceMentorPageView(LoginRequiredMixin, GetData, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'management/attendance-mentor.html'
    success_url = 'attendance_mentor'

    def form_valid(self, form):
        if form.is_valid():
            post_objects = zip(
                self.request.POST.getlist('group_member_id'),
                self.request.POST.getlist('group_id'),
                self.request.POST.getlist('date'),
                self.request.POST.getlist('condition')
            )
            post_objects = list(post_objects)
            # Checking date
            checked_date = []
            for check_date in Attendance.objects.values('date'):
                if self.request.POST['date'] == str(check_date['date']):
                    checked_date.append(self.request.POST['date'])
            # Create attendance
            for post_object in post_objects:
                if not post_object[2] in checked_date:
                    attendance_data = Attendance(
                        group_member_id=GroupMember.objects.get(pk=post_object[0]),
                        group_id=CourseGroup.objects.get(pk=post_object[1]),
                        date=post_object[2],
                        condition=post_object[3],
                    )
                    attendance_data.save()
            return redirect('attendance_mentor')
        else:
            print('--form invalid--')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = CourseGroup.objects.filter(mentor_id=self.request.user.id)
        context['groups'] = group
        return context
    
class FilterAttendanceMentorPageView(AttendanceMentorPageView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            filter_group = CourseGroup.objects.get(name=self.request.GET['fgroup'])
            if filter_group:
                context['members'] = GroupMember.objects.filter(group_id=filter_group)
        except:
            pass
        return context


class AttendanceAdminPageView(LoginRequiredMixin, GetData, TemplateView):
    template_name = 'management/attendance-admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendance'] = Attendance.objects.filter(condition__in=[1, 2])
        return context
    

class AttendanceEditView(LoginRequiredMixin, GetData, UpdateView):
    model = Attendance
    form_class = AttendanceEditForm
    success_url = reverse_lazy('attendance_admin')
    template_name = 'management/attendance-edit.html'


class AttendanceDeleteView(LoginRequiredMixin, GetData, DeleteView):
    model = Attendance
    success_url = reverse_lazy('attendance_admin')
    template_name = 'management/attendance-delete.html'


class CompanyEditView(LoginRequiredMixin, GetData, UpdateView):
    model = CompanyInfo
    form_class = CompanyEditForm
    success_url = reverse_lazy('home_page')
    template_name = 'management/company-edit.html'


class PermissionsPageView(LoginRequiredMixin, GetData, TemplateView):
    template_name = 'management/permissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context
    

def download_check(request, check_id):
    uploaded_file = Payment.objects.get(pk=check_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response


@login_required
def permission_add(request, group_id):
    permission_data = GroupMember(
        group_id=CourseGroup.objects.get(pk=group_id),
        student_id=Profile.objects.get(user_id=request.user.id),
        permission="0"
    )
    permission_data.save()
    return redirect('my_courses')


class PermissionEditView(LoginRequiredMixin, GetData, UpdateView):
    model = GroupMember
    form_class = PermissionEditForm
    success_url = reverse_lazy('permissions')
    template_name = 'management/permission-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.filter(group_member_id=self.kwargs.get('pk'))
        context['member'] = GroupMember.objects.get(pk=self.kwargs.get('pk'))
        context['members'] = GroupMember.objects.filter(student_id=context['member'].student_id, permission="1")
        return context
    

class MessagesPageView(LoginRequiredMixin, GetData, ListView):
    paginate_by = 6
    model = Feedback
    template_name = 'management/messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Feedback.objects.all().order_by('created_at')
        return context


class Error404PageView(TemplateView):
    template_name = '404.html'


class Error500PageView(TemplateView):
    template_name = '500.html'
