from django.contrib import admin  # admin site
from django.contrib.auth import views as auth_views  # built-in login/logout views
from django.urls import path, include  # URL routing helpers
from users import views as user_views  # custom user views
from django.conf import settings
from django.conf.urls.static import static  # serve media files in dev
from rest_framework import routers
from users.api import UserProfileViewSet
from courses.api import CourseViewSet, FeedbackViewSet
from chat.api import MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # your existing routes...
    path("api/", include(router.urls)),  # REST API endpoints
]

urlpatterns = [
    path('admin/', admin.site.urls),  # admin interface
    path('', user_views.landing, name='home'),  # landing page
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path("", include("chat.urls")),
    path('signup/', user_views.signup, name='signup'),  # registration
    path('home/', user_views.home, name='router'),  # redirect to dashboard
    path('teacher_dashboard/', user_views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', user_views.student_dashboard, name='student_dashboard'),
    path("courses/", include("courses.urls")),  # course-related routes
    path("api/", include(router.urls)),  # REST API endpoints
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
