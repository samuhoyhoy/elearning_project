from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile
from courses.models import (
    Course, Enrollment, Feedback as FeedbackModel, StatusUpdate,
    Notification, BlockedStudent
)
from django.db import IntegrityError

# helper to quickly create a UserProfile
def make_profile(username, real_name, role):
    auth = User.objects.create_user(username=username, password='pw')
    return UserProfile.objects.create(user=auth, real_name=real_name, role=role)


class CourseModelTests(TestCase):
    def setUp(self):
        self.teacher = make_profile('teach', 'Teacher', 'teacher')

    def test_course_str(self):
        # __str__ should return course title
        course = Course.objects.create(title='Demo', description='desc', teacher=self.teacher)
        self.assertEqual(str(course), 'Demo')


class EnrollmentTests(TestCase):
    def setUp(self):
        self.teacher = make_profile('teach', 'Teacher', 'teacher')
        self.student = make_profile('stud', 'Student', 'student')
        self.course = Course.objects.create(title='Demo', description='desc', teacher=self.teacher)

    def test_unique_enrollment(self):
        # same student/course pair should raise IntegrityError
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(student=self.student, course=self.course)

    def test_enrollment_str(self):
        # __str__ should mention "enrolled in"
        enr = Enrollment.objects.create(student=self.student, course=self.course)
        self.assertIn('enrolled in', str(enr))


class FeedbackTests(TestCase):
    def setUp(self):
        self.teacher = make_profile('teach', 'Teacher', 'teacher')
        self.student = make_profile('stud', 'Student', 'student')
        self.course = Course.objects.create(title='Demo', description='desc', teacher=self.teacher)

    def test_feedback_str(self):
        # __str__ should mention "Feedback by"
        fb = FeedbackModel.objects.create(student=self.student, course=self.course, comment='nice', rating=4)
        self.assertIn('Feedback by', str(fb))


class StatusNotificationTests(TestCase):
    def setUp(self):
        self.user = make_profile('user', 'User', 'student')

    def test_status_str_and_creation(self):
        # __str__ should include user name
        su = StatusUpdate.objects.create(user=self.user, content='hello world')
        self.assertIn('User:', str(su))

    def test_notification_default(self):
        # new notifications should default to unread
        note = Notification.objects.create(user=self.user, message='hi')
        self.assertFalse(note.read)


class BlockedStudentTests(TestCase):
    def setUp(self):
        self.teacher = make_profile('teach', 'Teacher', 'teacher')
        self.student = make_profile('stud', 'Student', 'student')
        self.course = Course.objects.create(title='Demo', description='desc', teacher=self.teacher)

    def test_block_str_global(self):
        # global block string should mention "globally blocked"
        blk = BlockedStudent.objects.create(teacher=self.teacher, student=self.student)
        self.assertIn('globally blocked', str(blk))

    def test_block_str_course(self):
        # course-specific block string should mention "blocked from"
        blk = BlockedStudent.objects.create(teacher=self.teacher, student=self.student, course=self.course)
        self.assertIn('blocked from', str(blk))
