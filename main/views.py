from django.shortcuts import render,redirect
from rancikeCms import settings
from django.views.decorators.csrf import csrf_exempt
from rancikeCms.settings import EMAIL_HOST_USER, BASE_URL
from django.core.mail import send_mail, send_mass_mail
from django.contrib import messages
import threading
from threading import Thread
from register_login.models import Teacher,School,User1
from register_login.models import Intern
from questions.models import Question
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def home(request):
    data = {}
    user = request.user
    if user.is_active:
        if not user.is_teacher and not user.is_school :
            data["profile_completion"] = True


    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')
        recievers = []
        message = "new Message From "+name+ ' email :' +email+ "\n  message :"+ message
        recievers.append(EMAIL_HOST_USER)
        subject = "New Query From Question Portal"
        EmailThread(subject,message,recievers).start()
        # send_mail(subject, message, EMAIL_HOST_USER, recievers)
        messages.info(request,"Thank You We will Reach out to you soon")
        return redirect('home')
    return render(request, 'landing.html',data)


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.message = message
        threading.Thread.__init__(self)

    def run (self):
        send_mail(self.subject, self.message, EMAIL_HOST_USER, self.recipient_list)
        # msg.send()

def complete_profile(request):

    user = request.user

    if request.method == "POST":
        if request.POST["type"] == "teacher":
            teach= Teacher()
            user.credit = 50
            teach.user=user
            teach.first_name=user.first_name
            teach.last_name=user.last_name
            teach.email=user.email
            user.save()            
            teach.save()
            User1.objects.filter(id=user.id).update(is_teacher = True)
            messages.info(request, "Information Saved")
           

        elif request.POST["type"] == "school":
            sch= School()
            user.credit = 100
            sch.user=user
            sch.school_name=user.school_name
            sch.location=user.location
            sch.email=user.email
            user.save()            
            sch.save()
            User1.objects.filter(id=user.id).update(is_school = True)
            messages.info(request, "Information Saved")
        return redirect("home")
    return render(request,"complete_profile.html")




def tnc(request):
    
    return render(request,"tnc.html")

def privacy(request):

    return render(request,"privacy.html")



def show_interns(request):
    if request.user.is_superuser:
        interns = Intern.objects.all()
        data = {"interns":interns}
        if request.method == "POST":
            id = request.POST.get("id")
            amount = request.POST.get("amount")
            user  = User1.objects.filter(id = id).first()
            intern = Intern.objects.filter(user = user).first()
            intern.amount_left = intern.amount_left - int(amount)
            intern.paid_for += int(amount)
            if intern.amount_left >= 0:
                intern.save()
            else:
                messages.error(request,"Balance can't be negative")
            return redirect('show_interns')
        return render(request,"show_interns.html",data)



def intern_details(request,username):


    user = User1.objects.filter(username = username).first()
    if request.user.is_staff:
        if request.method == "POST":
            
            id = request.POST['id']
            comments =  request.POST.get('comments')
            approval = request.POST.get('approval')
            question = Question.objects.filter(id=id)
            
            if approval == 'on':
                question.update(status = "Yes")
            if comments !="":
                recievers = []
                recievers.append(user.email)
                subject = "Revision to Question Requested for Question_ID : {}".format(id) 
                message =  "Please review Question_ID using the link below "+ id +"\n" + "https://cms.rancikelearning.com/admin/questions/question/" +id+ "/change/ \n" +comments
                EmailThread(subject,message,recievers).start()
                return redirect("intern_details",username)
        questions = Question.objects.filter(user=user)
        approved = questions.filter(status = "Yes")
        rejected = questions.filter(status = "No")

        data = {
            'approved':approved,
            'rejected':rejected
        }
        return render(request,"admin_questions.html",data)
    


def approve_questions(request):
    if request.user.is_staff:
        if request.method == "POST":
            if request.POST.get('date') is not None and len(request.POST.get('date'))!=0:
                date = request.POST.get('date')
                return redirect('approve_questions_date',date)
            id = request.POST['id']
            comments =  request.POST.get('comments')
            approval = request.POST.get('approval')
            question = Question.objects.filter(id=id)
            
            if approval == 'on':
                question.update(status = "Yes")
                
            if comments !="":
                recievers = []
                recievers.append(question.user.email)
                subject = "Revision to Question Requested"
                message =  "Please review Question_ID using the link below "+ id +"\n" + "https://cms.rancikelearning.com/admin/questions/question/" +id+ "/change/  \n"  +comments
                EmailThread(subject,message,recievers).start()
                return redirect("approve_questions",)
        rejected = Question.objects.filter(status='No')

        paginator = Paginator(rejected,20)
        page = request.GET.get('page')
        try:
            rejected = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer deliver the first page
            rejected = paginator.page(1)
        except EmptyPage:
        # If page is out of range deliver last page of results
            rejected = paginator.page(paginator.num_pages)
        data = {
            'rejected':rejected
        }
        return render(request,"admin_questions.html",data)
        


def approve_questions_date(request,date):

    if request.user.is_staff:
        if request.method == "POST":
            if request.POST.get('date') is not None and len(request.POST.get('date'))!=0:
                date = request.POST.get('date')
                return redirect('approve_questions_date',date)
            id = request.POST['id']
            comments =  request.POST.get('comments')
            approval = request.POST.get('approval')
            question = Question.objects.filter(id=id)
            
            if approval == 'on':
                question.update(status = "Yes")
            if comments !="":
                recievers = []
                recievers.append(question.user.email)
                subject = "Revision to Question Requested"
                message =  "Please review Question_ID using the link below "+ id +"\n" + "https://cms.rancikelearning.com/admin/questions/question/" +id+ "/change/  \n"  +comments
                EmailThread(subject,message,recievers).start()
                return redirect("approve_questions",)


        date_formatted = datetime.strptime(date, '%Y-%m-%d').date()
        rejected = Question.objects.filter(status='No').filter(created_at__date=date)
      
        data = {
            'rejected':rejected
        }
        return render(request,"admin_questions.html",data)