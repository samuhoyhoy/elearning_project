from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # roles available for users
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    # one-to-one link to Django's built-in User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # extra fields beyond the default User
    real_name = models.CharField(max_length=100)  # display name
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)  # optional avatar
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # determines dashboard/permissions

    def __str__(self):
        # show name + role in admin/debug
        return f"{self.real_name} ({self.role})"
