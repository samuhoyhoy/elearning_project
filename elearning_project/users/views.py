# standard shortcuts for rendering templates and redirecting
from django.shortcuts import render, redirect
# decorator to require login on views
from django.contrib.auth.decorators import login_required
# response helper for permission denial
from django.http import HttpResponseForbidden
# used for complex queries in search
from django.db.models import Q
from .forms import SignUpForm, UserSearchForm  # custom forms in users app
from .models import UserProfile  # profile extends built-in User
from courses.models import Notification, Enrollment, Course, BlockedStudent, StatusUpdate
from courses.forms import StatusUpdateForm  # form for posting status updates

def landing(request):
    # simple landing page showing buttons to login/signup
    return render(request, 'home.html')

@login_required
# dispatch user to appropriate dashboard based on their role
# called after login or via the 'home' named route

def home(request):
    profile = request.user.userprofile
    if profile.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')
    
@login_required
# dashboard view shown to a teacher after login
# collects various pieces of data to render the template

def teacher_dashboard(request):
    profile = request.user.userprofile
    # unread notifications for the sidebar
    notifications = Notification.objects.filter(user=profile, read=False).order_by('-created_at')

    # process status update form submission if posted
    status_form = StatusUpdateForm(request.POST or None)
    if request.method == 'POST' and status_form.is_valid():
        status = status_form.save(commit=False)
        status.user = profile
        status.save()
        return redirect('teacher_dashboard')

    # feed of the 20 most recent statuses across all users
    all_statuses = StatusUpdate.objects.order_by('-created_at')[:20]

    # search users form and results (teachers only)
    form = UserSearchForm(request.GET or None)
    results = []
    if form.is_valid():
        query = form.cleaned_data.get("query", "")
        role = form.cleaned_data.get("role", "")
        if query:
            results = UserProfile.objects.filter(
                Q(real_name__icontains=query) | Q(user__username__icontains=query)
            )
            if role:
                results = results.filter(role=role)
    # list of students this teacher has blocked globally, used to toggle unblock link
    blocked_student_ids = []
    if profile.role == 'teacher':
        from courses.models import BlockedStudent
        blocked_student_ids = list(
            BlockedStudent.objects.filter(teacher=profile)
            .values_list('student_id', flat=True)
        )

    # personal statuses (latest 10)
    statuses = StatusUpdate.objects.filter(user=profile).order_by('-created_at')[:10]

    return render(request, 'teacher_dashboard.html', {
        'profile': profile,
        'notifications': notifications,
        'form': form,
        'results': results,
        'blocked_student_ids': blocked_student_ids,
        'status_form': status_form,
        'statuses': statuses,
        'all_statuses': all_statuses,
    })

@login_required
# dashboard view for students: show courses, statuses, etc.
def student_dashboard(request):
    profile = request.user.userprofile
    # courses the student is enrolled in (prefetch course relation)
    enrollments = Enrollment.objects.filter(student=profile).select_related('course')
    # list of all courses (for enrolment display)
    all_courses = Course.objects.all()
    enrolled_course_ids = set(enrollments.values_list('course_id', flat=True))
    # unread notifications
    notifications = Notification.objects.filter(user=profile, read=False).order_by('-created_at')

    # status update handling
    status_form = StatusUpdateForm(request.POST or None)
    if request.method == 'POST' and status_form.is_valid():
        status = status_form.save(commit=False)
        status.user = profile
        status.save()
        return redirect('student_dashboard')

    statuses = StatusUpdate.objects.filter(user=profile).order_by('-created_at')[:10]
    all_statuses = StatusUpdate.objects.order_by('-created_at')[:20]

    return render(request, 'student_dashboard.html', {
        'profile': profile,
        'enrollments': enrollments,
        'all_courses': all_courses,
        'enrolled_course_ids': enrolled_course_ids,
        'notifications': notifications,
        'status_form': status_form,
        'statuses': statuses,
        'all_statuses': all_statuses,
    })

def signup(request):
    # signup form (GET shows form, POST creates user + profile)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                real_name=form.cleaned_data['real_name'],
                role=form.cleaned_data['role']
            )
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

