from django.db import models
from users.models import UserProfile

# Courses & Enrollment 
class Course(models.Model):
    title = models.CharField(max_length=200)              # course name
    description = models.TextField()                      # course details
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courses')  
    # teacher who owns the course

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='enrollments')  
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')  
    date_enrolled = models.DateTimeField(auto_now_add=True)  # auto timestamp

    def __str__(self): 
        return f"{self.student.real_name} enrolled in {self.course.title}"

    class Meta: 
        unique_together = ('student', 'course')  # prevent duplicate enrollments

# Notifications
class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="notifications")  
    message = models.TextField()                          # notification text
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp
    read = models.BooleanField(default=False)             # mark as read/unread

    def __str__(self):
        return f"Notification for {self.user.real_name}: {self.message}"

# Course Materials
class CourseMaterial(models.Model):
    course = models.ForeignKey("Course", related_name="materials", on_delete=models.CASCADE)  
    title = models.CharField(max_length=200, blank=True, null=True)  
    file = models.FileField(upload_to="course_materials/")  
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.title} ({self.course.title})"

# Blocking Students
class BlockedStudent(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blocked_students")  
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="blocked_students", null=True, blank=True)  
    # null = global block

    def __str__(self):
        if self.course:
            return f"{self.student.real_name} blocked from {self.course.title}"
        return f"{self.student.real_name} globally blocked"

# Feedback 
class Feedback(models.Model):
    student = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)  
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="feedbacks")  
    comment = models.TextField()  
    rating = models.PositiveIntegerField(default=5)       # 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Feedback by {self.student.real_name} on {self.course.title}"

# Status Updates
class StatusUpdate(models.Model):
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="status_updates")  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.real_name}: {self.content[:30]}"  # preview first 30 chars
