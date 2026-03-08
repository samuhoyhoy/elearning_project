from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Enrollment, Notification, CourseMaterial, Course

# Teacher notifications
@receiver(post_save, sender=Enrollment)
def notify_teacher_on_enroll(sender, instance, created, **kwargs):
    # when student enrolls
    if created:
        Notification.objects.create(
            user=instance.course.teacher,
            message=f"{instance.student.real_name} enrolled in {instance.course.title}"
        )

@receiver(post_delete, sender=Enrollment)
def notify_teacher_on_unenroll(sender, instance, **kwargs):
    # when student unenrolls
    Notification.objects.create(
        user=instance.course.teacher,
        message=f"{instance.student.real_name} unenrolled from {instance.course.title}"
    )

# Student notifications
@receiver(post_save, sender=CourseMaterial)
def notify_students_on_new_material(sender, instance, created, **kwargs):
    # when new material is added
    if created:
        for enrollment in instance.course.enrollments.all():
            Notification.objects.create(
                user=enrollment.student,
                message=f"New material in {instance.course.title}: {instance.file.name}"
            )

@receiver(post_save, sender=Course)
def notify_students_on_course_creation(sender, instance, created, **kwargs):
    # when a new course is created
    if created:
        from users.models import UserProfile
        for student in UserProfile.objects.filter(role='student'):
            Notification.objects.create(
                user=student,
                message=f"New course available: {instance.title}"
            )
