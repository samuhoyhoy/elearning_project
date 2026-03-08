from django import forms
from .models import Course, CourseMaterial, Feedback, StatusUpdate

# form for creating/editing courses
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

# form for uploading course materials
class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ["title", "file"]

# form for student feedback (with rating)
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["comment", "rating"]

# form for posting status updates
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ["content"]
