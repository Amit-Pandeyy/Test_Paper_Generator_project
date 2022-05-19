from django.contrib import admin
from django.urls import path, include
from .views import home,complete_profile,tnc,privacy,show_interns,approve_questions_date,intern_details,approve_questions


urlpatterns = [
    path('',home,name="home"),
    path('generatePDF/',include('generatePDF.urls')),
    path('upload_question/',include('upload_question.urls')),
    path('paper/', include('QuestionPaper.urls')),
    path('payment/', include('payment.urls')),
    path("complete_profile",complete_profile,name="complete_profile"),
    path("tnc/",tnc,name="tnc"),
    path("privacy",privacy,name="privacy"),
    path('show_interns',show_interns,name="show_interns"),
    path("intern_detail/<str:username>",intern_details,name="intern_details"),
    path('approve_questions',approve_questions,name='approve_questions'),
    path('approve_questions_date/<str:date>',approve_questions_date,name="approve_questions_date")
]
