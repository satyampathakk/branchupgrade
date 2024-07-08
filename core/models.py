# core/models.py
from django.db import models
from django.contrib.auth.models import User

# Define branch choices as a tuple of tuples
BRANCH_CHOICES = [
    ('CSE', 'Computer Science and Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('EE', 'Electrical Engineering'),
    ('CE', 'Civil Engineering'),
    ('CHE', 'Chemical Engineering'),
    ('ECE', 'Electronics and Communication Engineering'),
]
CATEGORY_CHOICES = [
    ('open', 'Open'),
    ('open_pwd', 'Open PWD'),
    ('ews', 'Economically Weaker Section'),
    ('ews_pwd', 'EWS PWD'),
    ('sc', 'Scheduled Caste'),
    ('sc_pwd', 'SC PWD'),
    ('st', 'Scheduled Tribe'),
    ('st_pwd', 'ST PWD'),
    ('obc_ncl', 'Other Backward Class (Non-Creamy Layer)'),
    ('obc_ncl_pwd', 'OBC NCL PWD')
]
class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True)
    cgpa = models.FloatField()
    email=models.CharField(max_length=50,default='')
    jee_rank = models.IntegerField()
    category = models.CharField(max_length=50)
    preference1 = models.CharField(max_length=50, choices=BRANCH_CHOICES, blank=True, null=True)
    preference2 = models.CharField(max_length=50, choices=BRANCH_CHOICES, blank=True, null=True)
    preference3 = models.CharField(max_length=50, choices=BRANCH_CHOICES, blank=True, null=True)
    allocated_branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, blank=True, null=True)


class Vacancy(models.Model):
    branch_name = models.CharField(max_length=50, choices=BRANCH_CHOICES, unique=True)
    open_seats = models.IntegerField(default=0)
    open_pwd_seats = models.IntegerField(default=0)
    ews_seats = models.IntegerField(default=0)
    ews_pwd_seats = models.IntegerField(default=0)
    sc_seats = models.IntegerField(default=0)
    sc_pwd_seats = models.IntegerField(default=0)
    st_seats = models.IntegerField(default=0)
    st_pwd_seats = models.IntegerField(default=0)
    obc_ncl_seats = models.IntegerField(default=0)
    obc_ncl_pwd_seats = models.IntegerField(default=0)
    def __str__(self):
        return self.branch_name
    def __str__(self):
        return self.branch_name
    def total_seats(self):
        return (self.open_seats + self.open_pwd_seats + self.ews_seats + self.ews_pwd_seats +
                self.sc_seats + self.sc_pwd_seats + self.st_seats + self.st_pwd_seats +
                self.obc_ncl_seats + self.obc_ncl_pwd_seats)