from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .models import Course, Enrollment, Notification, BlockedStudent, CourseMaterial, Feedback
from .forms import CourseForm, CourseMaterialForm, FeedbackForm
from users.models import UserProfile
from django.http import JsonResponse 

# helper: check if user is a teacher
def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'teacher'

@user_passes_test(is_teacher)
def create_course(request):
    # quick course creation (title/desc only)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        teacher_profile = request.user.userprofile
        Course.objects.create(title=title, description=description, teacher=teacher_profile)
        return redirect('course_list')
    return render(request, 'courses/create_course.html')

@login_required
def add_course(request):
    # teachers can add courses via form
    if request.user.userprofile.role != 'teacher':
        return redirect('home')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.userprofile
            course.save()
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})

@login_required
def delete_course(request, course_id):
    # only teacher who owns course can delete
    profile = request.user.userprofile
    if profile.role != 'teacher':
        return redirect('home')
    course = get_object_or_404(Course, id=course_id, teacher=profile)
    course.delete()
    return redirect('teacher_dashboard')

@login_required
def add_material(request, course_id):
    # teacher uploads course material
    course = get_object_or_404(Course, id=course_id, teacher=request.user.userprofile)
    if request.method == "POST":
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            return redirect("teacher_dashboard")
    else:
        form = CourseMaterialForm()
    return render(request, "courses/add_material.html", {"form": form, "course": course})

@login_required
def delete_material(request, material_id):
    # only teacher who owns course can delete material
    profile = request.user.userprofile
    material = get_object_or_404(CourseMaterial, id=material_id)
    if profile.role == "teacher" and material.course.teacher == profile:
        material.delete()
    return redirect("teacher_dashboard")

def course_list(request):
    # show all courses + mark which ones student is enrolled in
    courses = Course.objects.all()
    previous_url = request.META.get('HTTP_REFERER', '/')

    enrolled_course_ids = set()
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and \
       request.user.userprofile.role == 'student':
        enrolled_course_ids = set(
            Enrollment.objects.filter(student=request.user.userprofile)
                      .values_list('course_id', flat=True)
        )

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'previous_url': previous_url,
        'enrolled_course_ids': enrolled_course_ids,
    })

@login_required
def enrol_course(request, course_id):
    # student enrolls in course (unless blocked)
    profile = request.user.userprofile
    course = get_object_or_404(Course, id=course_id)
    if profile.role != "student":
        return redirect("home")

    from django.db.models import Q
    if BlockedStudent.objects.filter(
        student=profile,
        teacher=course.teacher,
    ).filter(Q(course=course) | Q(course__isnull=True)).exists():
        messages.error(request, "You are blocked from enrolling in this course.")
        return redirect("student_dashboard")

    Enrollment.objects.get_or_create(student=profile, course=course)
    messages.success(request, f"You have successfully enrolled in {course.title}.")
    return redirect("student_dashboard")

@login_required
def unenroll_course(request, course_id):
    # student unenrolls from course
    enrollment = get_object_or_404(
        Enrollment,
        student=request.user.userprofile,
        course_id=course_id
    )
    enrollment.delete()
    return redirect('student_dashboard')

@login_required
def get_notifications(request):
    # return unread notifications as JSON
    profile = request.user.userprofile
    notes = Notification.objects.filter(user=profile, read=False).order_by('-created_at')
    data = [
        {"id": n.id, "message": n.message, "created_at": n.created_at.strftime("%b %d, %Y %I:%M %p")}
        for n in notes
    ]
    return JsonResponse({"notifications": data})

@login_required
def mark_notification_read(request, note_id):
    # mark notification as read, redirect to dashboard
    note = get_object_or_404(Notification, id=note_id, user=request.user.userprofile)
    note.read = True
    note.save()
    if request.user.userprofile.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')
    
@login_required
def remove_student(request, course_id, student_id):
    # teacher removes student from course
    profile = request.user.userprofile
    if profile.role != "teacher":
        return redirect("home")
    course = get_object_or_404(Course, id=course_id, teacher=profile)
    enrollment = get_object_or_404(Enrollment, course=course, student_id=student_id)
    enrollment.delete()
    return redirect("teacher_dashboard")

@login_required
def block_student_global(request, student_id):
    # teacher blocks student globally
    teacher = request.user.userprofile
    student = get_object_or_404(UserProfile, id=student_id, role="student")
    BlockedStudent.objects.get_or_create(teacher=teacher, student=student, course=None)
    return redirect("teacher_dashboard")

@login_required
def unblock_student_global(request, student_id):
    # teacher unblocks student globally
    teacher = request.user.userprofile
    blocked = get_object_or_404(
        BlockedStudent,
        teacher=teacher,
        student_id=student_id,
        course__isnull=True,
    )
    blocked.delete()
    return redirect("teacher_dashboard")

@login_required
def add_feedback(request, course_id):
    # student leaves feedback on course
    course = get_object_or_404(Course, id=course_id)
    profile = request.user.userprofile
    if profile.role != "student":
        return redirect("home")

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = profile
            feedback.course = course
            feedback.save()
            return redirect("student_dashboard")
    else:
        form = FeedbackForm()
    return render(request, "courses/add_feedback.html", {"form": form, "course": course})

@login_required
def delete_feedback(request, feedback_id):
    # teacher deletes feedback on their course
    feedback = get_object_or_404(Feedback, id=feedback_id)
    profile = request.user.userprofile
    if profile.role == "teacher" and feedback.course.teacher == profile:
        feedback.delete()
    return redirect("teacher_dashboard")
