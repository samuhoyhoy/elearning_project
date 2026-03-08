from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserProfile
from users.forms import SignUpForm, UserSearchForm

class UserAccountTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        # Posting signup form should create a User + UserProfile
        data = {
            'username': 'newuser',
            'real_name': 'New User',
            'role': 'student',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertRedirects(response, reverse('login'))  # redirect after signup
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.real_name, 'New User')
        self.assertEqual(profile.role, 'student')

    def test_signup_form_validation(self):
        # Form should fail if passwords don't match
        form = SignUpForm(
            data={
                'username': 'foo',
                'real_name': 'Foo Bar',
                'role': 'teacher',
                'password1': 'abc',
                'password2': 'xyz',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_user_search_form(self):
        # Search form works with empty or filled data
        form = UserSearchForm(data={})
        self.assertTrue(form.is_valid())
        form = UserSearchForm(data={'query': 'bob', 'role': 'student'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['query'], 'bob')

    def test_teacher_can_search_users_via_dashboard(self):
        # Teacher dashboard search should return matching users
        teacher = User.objects.create_user(username='teach', password='pass')
        UserProfile.objects.create(user=teacher, real_name='Teach', role='teacher')
        student = User.objects.create_user(username='stud', password='pass')
        UserProfile.objects.create(user=student, real_name='Stud', role='student')

        self.client.login(username='teach', password='pass')
        response = self.client.get(reverse('teacher_dashboard'), {'query': 'Stud'})
        self.assertEqual(response.status_code, 200)
        results = response.context['results']
        self.assertTrue(any(u.real_name == 'Stud' for u in results))
