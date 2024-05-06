from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'failed': 'Login failed. Incorrect username or password.'})
        
    else:
        return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

'''
FOR CREATING USERS WITH ELEVATED ACCESS FOR ALLOWING CHANGES
------------------------------------------------------------


def create_new_user(request):
    UnitCoordinator = User.objects.create_user("UnitCoordinator", "", "unitcoordinator")
    Supervisor = User.objects.create_user("Supervisor", "", "supervisor")
    Student = User.objects.create_user("Student", "", "student")
    return render(request, 'users/login.html')
'''

'''
FOR ADDING PERMISSIONS FOR USERS
--------------------------------
def add_permissions(request):
    user = User.objects.get(username = 'UnitCoordinator')
    permissions = Permission.objects.get(codename__in = [
        'add_user', 'change_user', 'delete_user', 'view_user', 
        'add_campus','change_campus', 'delete_campus', 'view_campus',
        'add_category', 'change_category', 'delete_category', 'view_category',
        'add_course', 'change_course', 'delete_course', 'view_course',
        'add_supervisor', 'change_supervisor', 'delete_supervisor', 'view_supervisor',
         
    ])
    print(permissions)
    user.user_permissions.add(permissions)
    
    all_permissions = Permission.objects.all()

    for permission in all_permissions:
        print(f'{permission} - {permission.codename}')
    return render(request, 'users/login.html')
'''
