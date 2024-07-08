# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Student, BRANCH_CHOICES, CATEGORY_CHOICES, Vacancy

def update_preferences(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')
        cgpa = request.POST.get('cgpa')
        jee_rank = request.POST.get('jee_rank')
        category = request.POST.get('category')
        preference1 = request.POST.get('preference1')
        preference2 = request.POST.get('preference2')
        preference3 = request.POST.get('preference3')

        if not roll_no:
            return HttpResponse("Roll number is required.", status=400)

        try:
            cgpa = float(cgpa)
            jee_rank = int(jee_rank)
        except ValueError:
            return HttpResponse("Invalid CGPA or JEE Rank.", status=400)

        try:
            student = Student.objects.get(roll_no=roll_no)
            message = "Preferences updated successfully."
        except Student.DoesNotExist:
            student = Student(roll_no=roll_no)
            message = "Student created and preferences set successfully."

        student.cgpa = cgpa
        student.jee_rank = jee_rank
        student.category = category
        student.preference1 = preference1
        student.preference2 = preference2
        student.preference3 = preference3
        student.save()

        return HttpResponse(message)
    else:
        return render(request, 'student_portal.html', {
            'branch_choices': BRANCH_CHOICES,
            'category_choices': CATEGORY_CHOICES
        })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_portal')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def admin_portal(request):
    students = Student.objects.all()
    vacancies = Vacancy.objects.all()

    if request.method == 'POST' and 'publish' in request.POST:
        # Logic to publish results and allocate branches
        allocated_students = allocate_branches(students, vacancies)

        # Update the allocated branch for each student
        for student, branch in allocated_students.items():
            student.allocated_branch = branch
            student.save()

        return render(request, 'admin_portal.html', {
            'students': students, 'vacancies': vacancies, 'message': 'Results published successfully'
        })

    return render(request, 'admin_portal.html', {
        'students': students, 'vacancies': vacancies
    })

def allocate_branches(students, vacancies):
    # Logic to allocate branches based on CGPA criteria
    allocated_students = {}

    # Sort students by CGPA descending
    sorted_students = sorted(students, key=lambda s: s.cgpa, reverse=True)

    # Iterate over sorted students and allocate branches
    for student in sorted_students:
        for vacancy in vacancies:
            if can_allocate(student, vacancy):
                allocated_students[student] = vacancy.branch_name
                # Reduce the available seats for the allocated branch
                update_vacancy(vacancy)
                break  # Move to the next student

    return allocated_students

def can_allocate(student, vacancy):
    # Check if the student meets the criteria for the vacancy
    if student.allocated_branch or student.preference1:
        return False
    if student.preference1 not in vacancy.branch_name:
        return False
    return True

def update_vacancy(vacancy):
    # Reduce the available seats for the allocated branch
    vacancy.open_seats -= 1

    # Save the updated vacancy instance
    vacancy.save()

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def update_vacancy(request):
    if request.method == 'POST':
        try:
            # List of branches to iterate over
            branches = [
                ('CSE', 'Computer Science and Engineering'),
                ('ME', 'Mechanical Engineering'),
                ('EE', 'Electrical Engineering'),
                ('CE', 'Civil Engineering'),
                ('CHE', 'Chemical Engineering'),
                ('ECE', 'Electronics and Communication Engineering'),
            ]

            for branch_code, branch_name in branches:
                # Try to get the vacancy for the current branch
                try:
                    vacancy = Vacancy.objects.get(branch_name=branch_name)
                except Vacancy.DoesNotExist:
                    # If vacancy does not exist, create a new one with default values
                    vacancy = Vacancy(branch_name=branch_name)

                # Update the vacancy fields from the POST data
                vacancy.open_seats = int(request.POST.get(f'open_seats_{branch_code.lower()}', 0))
                vacancy.open_pwd_seats = int(request.POST.get(f'open_pwd_seats_{branch_code.lower()}', 0))
                vacancy.ews_seats = int(request.POST.get(f'ews_seats_{branch_code.lower()}', 0))
                vacancy.ews_pwd_seats = int(request.POST.get(f'ews_pwd_seats_{branch_code.lower()}', 0))
                vacancy.sc_seats = int(request.POST.get(f'sc_seats_{branch_code.lower()}', 0))
                vacancy.sc_pwd_seats = int(request.POST.get(f'sc_pwd_seats_{branch_code.lower()}', 0))
                vacancy.st_seats = int(request.POST.get(f'st_seats_{branch_code.lower()}', 0))
                vacancy.st_pwd_seats = int(request.POST.get(f'st_pwd_seats_{branch_code.lower()}', 0))
                vacancy.obc_ncl_seats = int(request.POST.get(f'obc_ncl_seats_{branch_code.lower()}', 0))
                vacancy.obc_ncl_pwd_seats = int(request.POST.get(f'obc_ncl_pwd_seats_{branch_code.lower()}', 0))
                
                # Save the vacancy instance
                vacancy.save()

            return redirect('admin_portal')

        except ValueError:
            return HttpResponse("Invalid input for vacancy seats.", status=400)

    return redirect('admin_portal')