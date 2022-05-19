from register_login.models import User1
from django.shortcuts import redirect, render
from QuestionPaper.models import Paper
from django.contrib import messages
from rancikeCms.settings import  EMAIL_HOST_USER, BASE_URL
from django.core.mail import EmailMultiAlternatives
import threading
from threading import Thread
from django.contrib.auth.decorators import login_required
from register_login.decorators import teacher_required
from .models import Order,OrderItem
from questions.models import Question
from rancikeCms.settings import COST_PER_QUESTION
# Create your views here.


def get_total_marks(test):
    total = 0
    for ques in test:
        total += ques.marks
    return total

def send_order_email(request, order):

    # order_items = OrderItem.objects.filter(order=order)
  
    # order_items = zip(order_items, li)
    subject = 'Order Confirmed'
    # body_html = render_to_string('order_email.html', {})
    body_html ="<h1>Test Generated </h1> " + "<p> Thanks for using Edu Learning Portal</p>"
    from_email = EMAIL_HOST_USER
    to_email = order.user.email

    msg = EmailMultiAlternatives(
        subject,
        body_html,
        from_email=from_email,
        to=[to_email,from_email,]
    )

    msg.mixed_subtype = 'related'
    msg.attach_alternative(body_html, "text/html")

    msg.send()


class EmailThread(threading.Thread):
    def __init__(self, request, order):
        self.request = request
        self.order = order
        threading.Thread.__init__(self)

    def run(self):
        send_order_email(self.request, self.order)
        # msg.send()


def get_total_points(user):
    paper = Paper.objects.filter(user=user)
    totalitems = len(paper)
    points = totalitems*COST_PER_QUESTION 
    count=0
    for question in paper:
        if question.question.user == user:
            count+=1
    points-=count*COST_PER_QUESTION 
    return points

def clear_cart(user):
    test = Paper.objects.filter(user=user)
    for i in test:
        i.delete()
    
@login_required
@teacher_required
def checkout(request):
    user = request.user
    test = Paper.objects.filter(user=user)
    if len(test)<=0:
        messages.error(request,"Test is empty Please add questions first")
        return redirect("select_class")

    points_available = user.credit
    points_used = get_total_points(user)
    if(points_available<points_used):
        messages.error(request,"Not enough points available! Please recharge")
        return redirect("teacher_dashboard")

    
    total_marks = int(get_total_marks(test)) 

    if request.method == "POST" :
        test_name = request.POST.get("test_name")
        institute_name = request.POST.get("institute_name")
        paper_code =     request.POST.get("paper_code")
        subject_code =   request.POST.get("subject_code")
        description =   request.POST.get("description")
        guidelines =    request.POST.get("guidelines")
        order = Order(user=user,test_name = test_name,institute_name=institute_name,description=description,paper_code=paper_code,subject_code=subject_code,guidelines=guidelines)
        order.total_cost = points_used
        order.total_marks = total_marks
        order.save()
        save_questions_in_test(order,test)
        user.credit-=points_used
        user.save()
        clear_cart(user)
        messages.info(request,"test Generation successful!")
        return redirect('generatePDF',order_id=order.id)
    return render(request,"checkout.html")



def save_questions_in_test(order,test):
    for i in test:
        question = Question.objects.filter(id = i.question.id).first()
        OrderItem.objects.create(order=order,question=question,price=COST_PER_QUESTION,marks=i.marks)