from django.conf import settings
from django.shortcuts import render
from orders.models import Order,OrderItem
from register_login.models import Teacher
from django.contrib.auth.decorators import login_required
from register_login.decorators import teacher_required

# Create your views here.

@login_required
@teacher_required
def teacher_dashboard(request):

    user = request.user
    papers = Order.objects.filter(user=user)
    account = Teacher.objects.filter(user=user).first()

    data = {
        "account":account,
        "papers":papers,
        "total_papers":len(papers),
    }
    return render(request,"teacher_dashboard.html",data)

@login_required
@teacher_required
def show_old_paper(request,id):
    order = Order.objects.filter(id=id).first()
    questions = OrderItem.objects.filter(order=order)
    data ={
        "order":order,
        "questions":questions,
    }
    return render(request, 'generatePDF.html', data)
