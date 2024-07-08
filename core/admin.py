# core/admin.py
from django.contrib import admin
from .models import Student, Vacancy

admin.site.register(Student)
admin.site.register(Vacancy)
