from django.contrib import admin
from .models import Course, Enrollment, Feedback, StatusUpdate

# register models in Django admin
admin.site.register(Course)        # manage courses
admin.site.register(Enrollment)    # manage enrollments
admin.site.register(Feedback)      # manage feedback
admin.site.register(StatusUpdate)  # manage status updates
