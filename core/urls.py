# core/urls.py
from django.urls import path
from .views import login_view, admin_portal, logout_view, update_preferences, update_vacancy

urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin_portal/', admin_portal, name='admin_portal'),
    path('student/', update_preferences, name='student_portal'),
    path('update-preferences/', update_preferences, name='update_preferences'),
    path('update_vacancy/', update_vacancy, name='update_vacancy'),
    path('logout/', logout_view, name='logout'),
]
