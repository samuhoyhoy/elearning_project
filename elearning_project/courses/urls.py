from django.urls import path, include
from . import views
from rest_framework import routers
from users.api import UserProfileViewSet

urlpatterns = [ 
    path('create_course/', views.create_course, name='create_course'), # quick course creation   
    path('add_course/', views.add_course, name='add_course'), # add course via full form          
    path("courses/<int:course_id>/delete/", views.delete_course, name="delete_course"), # delete a specific course    
    path("courses/<int:course_id>/materials/add/", views.add_material, name="add_material"), # add material to a course  
    path("materials/<int:material_id>/delete/", views.delete_material, name="delete_material"), # delete a specific material   
    path('course_list/', views.course_list, name='course_list'), # list all available courses         
    path('enrol/<int:course_id>/', views.enrol_course, name='enrol_course'), # student enrols in a course
    path('notifications/', views.get_notifications, name='get_notifications'), # view all notifications  
    path('notifications/<int:note_id>/read/', views.mark_notification_read, name='mark_notification_read'), # mark a notification as read 
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'), # student unenrols from a course  
    path("courses/<int:course_id>/remove_student/<int:student_id>/", # teacher removes a student from a course 
         views.remove_student, name="remove_student"),  
    path("block_student/<int:student_id>/", views.block_student_global, name="block_student_global"),  # block student globally (all courses) 
    path("unblock_student/<int:student_id>/", views.unblock_student_global, name="unblock_student_global"),# unblock student globally 
    path("<int:course_id>/feedback/", views.add_feedback, name="add_feedback"), # add feedback for a course  
    path("feedback/<int:feedback_id>/delete/", views.delete_feedback, name="delete_feedback"), # delete specific feedback
]
