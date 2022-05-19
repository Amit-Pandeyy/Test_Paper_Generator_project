from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from register_login.models import School,Teacher,User1
from django.http import JsonResponse
from register_login.decorators import school_required
from django.contrib import messages

# Create your views here.
@login_required
@school_required 
def add_teacher(request):
    if request.method == 'POST':
        teacher_email = request.POST['email']
        account=User1.objects.filter(email = teacher_email).first()
        find_teacher = Teacher.objects.filter(user = account).first()
        if find_teacher is not None:
            school=request.user
            find_school = School.objects.filter(user = school).first()
            find_school.teachers.add(find_teacher)
            messages.info(request, "Teacher Added successfully")
        else:
            messages.info(request, "Email you entered is not registered with us")
    return render(request,'add_teacher.html')

@login_required
@school_required 
def show_teachers(request):
    data={}
    school=request.user
    find_school = School.objects.filter(user = school).first()
    if find_school is not None:
        teachers_in_school=find_school.teachers.all()
        data = {
            'teachers_in_school':teachers_in_school,
            'find_school':find_school,
            'number_of_teachers':len(teachers_in_school)
        }
        return render(request,'show_teachers.html',data)
    else: 
        return render(request,'show_teachers.html',data)

@login_required
@school_required 
def increase_credits(request):
    if request.method == 'GET':
        username = request.GET['username']
        increase_value = int(request.GET['increase_value'])
        find_user = User1.objects.filter(username = username).first()
        find_teacher = Teacher.objects.filter(user = find_user).first()
        school=request.user
        find_school = School.objects.filter(user = school).first()
        print(find_teacher)
        print(find_school)
        if ((increase_value > 0) and (find_school.user.credit-increase_value >= 0)):
            find_teacher.user.credit += increase_value
            find_teacher.user.save()
            find_school.user.credit -= increase_value 
            find_school.user.save()
            data = {
            'is_valid': True,
            'school_credits': find_school.user.credit,
            'teacher_credits': find_teacher.user.credit,
            }
            print(data)
            return JsonResponse(data)