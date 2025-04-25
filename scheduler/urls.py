from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Default route
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # Admin Functions
    path('add_course/', views.add_course, name='add_course'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('add_topic/', views.add_topic, name='add_topic'),
    
    # User Functions
    path('topic/<int:topic_id>/add-time/', views.add_time, name='add_time'),
    path('topic/<int:topic_id>/mark-done/', views.mark_done, name='mark_done'),
    path('progress/', views.user_progress, name='user_progress'),
]
