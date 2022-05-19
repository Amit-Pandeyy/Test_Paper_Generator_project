from django.shortcuts import render
from .models import Option, Standard,Subject,Question,Solution,Topic,Chapter
from QuestionPaper.models import Paper 
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from register_login.decorators import teacher_required

# Create your views here.

@login_required
@teacher_required
def select_class(request):

    standards = Standard.objects.annotate(subject_count =Count('subject', distinct=True)).annotate(question_count = Count('Question', filter=Q(Question__status = "Yes"),distinct=True))

    data = {
        'standards':standards
    }


    return render(request,'select_class.html',data)

@login_required
@teacher_required
def select_subject(request,standard_name):
    
    standard =  Standard.objects.filter(name = standard_name).first()
    subjects = Subject.objects.filter(standard = standard).annotate(Count('chapter', distinct=True)).annotate(question_count = Count('Question', filter=Q(Question__status = "Yes"),distinct=True))
    data = {
        'subjects':subjects,
        'standard_name':standard_name,
    }

    return render(request,"select_subject.html",data)

@login_required
@teacher_required
def select_chapter(request,standard_name,subject_name):

    standard = Standard.objects.filter(name = standard_name).first()
    subject = Subject.objects.filter(name = subject_name).first()
    chapters =  Chapter.objects.filter(standard = standard).filter(subject = subject).annotate(question_count = Count('Question', filter=Q(Question__status = "Yes"),distinct=True))
    data = {
        'chapters':chapters,
        'standard_name':standard_name,
        'subject_name':subject_name,
    }
    return render(request,'select_chapter.html',data)


@login_required
@teacher_required
def question_list(request,standard_name,subject_name,chapter_name,chapter_id):
    
    standard = Standard.objects.filter(name=standard_name).first()
    subject = Subject.objects.filter(name=subject_name).first()
    chapter = Chapter.objects.filter(name = chapter_name).first()
    questions = Question.objects.filter(standard = standard).filter(subject = subject).filter(chapter= chapter).filter(status="Yes")
    topics = Topic.objects.filter(standard = standard).filter(subject = subject).filter(chapter= chapter)

    difficulty = ['basic', 'easy', 'medium', 'hard']

   
    data = {
        "chapter_id":chapter_id,
        "questions":questions,
        "topics":topics,
        'difficulty': difficulty,
        "do_not_show_base_navbar":True,
    }
    return render(request,"question_list.html",data)

@login_required
@teacher_required
def question_topic_selector(request):

    if request.method == "GET":
        topic_id = request.GET.get('topic_id')
        if(topic_id):
            questions = Question.objects.filter(topic__id = topic_id).filter(status="Yes")
            paper = []
            if request.user.is_authenticated:
                items = Paper.objects.filter(user = request.user)
                paper = [p.question.id for p in items]
            returnData =  serializers.serialize('json',list(questions))
            data = {
                'questions':returnData,
                'paper':paper,
            }
            return JsonResponse(data)

@login_required
@teacher_required
def search_questions(request, chapter_id):
    if request.method == "GET":
        query = request.GET.get('query')
        questions=[]
        if len(query)>0:
            results = Question.objects.filter(chapter__id = chapter_id).filter(Q(title__icontains=query) | Q(text__icontains=query)).filter(status="Yes")
            questions =  serializers.serialize('json',list(results))
        paper = []
        if request.user.is_authenticated:
            items = Paper.objects.filter(user = request.user)
            paper = [p.question.id for p in items]
        data = {
                'questions':questions,
                'paper':paper,
            }
        return JsonResponse(data)

def get_question(request):
    if request.method == "GET":
        question_id = request.GET.get('que_id')
        question = Question.objects.filter(id = question_id).filter(status="Yes").first()
        options = Option.objects.filter(question = question)
        solution = Solution.objects.filter(question = question).first()
        if question:
            question =  serializers.serialize('json',[question])
        options =  serializers.serialize('json',list(options))
        if solution:
            solution =  serializers.serialize('json',[solution])
        data = {
                'question':question,
                'options':options,
                'solution':solution,
            }
        return JsonResponse(data)

