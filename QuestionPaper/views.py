from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from questions.models import OptionNumber, Question
from .models import Paper
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from register_login.decorators import teacher_required
from orders.models import Order, OrderItem
from rest_framework.views import APIView
from questions.models import Solution, Option



def get_total_points(user):
    paper = Paper.objects.filter(user=user)
    totalitems = len(paper)
    points = totalitems*settings.COST_PER_QUESTION 
    count=0
    for question in paper:
        if question.question.user == user:
            count+=1
    points-=count*settings.COST_PER_QUESTION 
    return points


# Create your views here.
@login_required
@teacher_required
def add_to_paper(request):

    if request.method == 'GET':
        que_id = request.GET['que_id']
        user = request.user
        question = Question.objects.get(id=que_id)
        Paper(user=user, question=question, marks = question.marks).save()
        data={
            'is_valid':True
        }
        return JsonResponse(data)


@login_required
@teacher_required
def show_paper(request):
    if request.user.is_authenticated:
        user = request.user
        questions_in_paper = Paper.objects.filter(user=user)
        total_marks = 0
        totalitem = len(questions_in_paper)
        print(get_total_points(user))
        if questions_in_paper:
            for p in questions_in_paper:
                total_marks+=p.marks
            return render(request, 'paper.html', {'questions_in_paper': questions_in_paper, 'total_marks': total_marks, 'totalitem': totalitem, 'points':get_total_points(user) ,"do_not_show_base_navbar":True,})
        else:
            return render(request, 'emptycart.html', {"do_not_show_base_navbar":True,})

@login_required
@teacher_required
def remove_paper(request):
    if request.method == 'GET':
        que_id = request.GET['que_id']

        c = Paper.objects.get(Q(question=que_id) & Q(user=request.user))
        c.delete()
        totalitem=0
        totalitem = len(Paper.objects.filter(user=request.user))

        total_marks = 0
        questions_in_paper = Paper.objects.filter(user=request.user)

        for p in questions_in_paper:
            total_marks+=p.question.marks

        data = {
            'is_valid':True,
            'total_marks': total_marks,
            'totalitem': totalitem,
            'points':get_total_points(request.user)
        }
        return JsonResponse(data)

@login_required
@teacher_required
def increase_marks(request):
    if request.method == 'GET':
        que_id = request.GET['que_id']

        c = Paper.objects.get(Q(question=que_id) & Q(user=request.user))
        c.marks += 1
        c.save()

        data = {
            'is_valid': True,
            'marks': c.marks
        }
      
        return JsonResponse(data)

@login_required
@teacher_required
def decrease_marks(request):
    if request.method == 'GET':
        que_id = request.GET['que_id']

        c = Paper.objects.get(Q(question=que_id) & Q(user=request.user))
        if c.marks>1:
            c.marks -= 1
            c.save()

            data = {
                'is_valid': True,
                'marks': c.marks
            }
        else:
            data = {
                'is_valid': False,
                'marks': c.marks
            }
      
        return JsonResponse(data)


from .serializers import QuestionSerializer, SolutionSerializer, OptionSerializer
from rest_framework.response import Response
from rest_framework .views import APIView

class get_quiz(APIView):
    def get(self, request, paper_code=None, format=None) :
        order = Order.objects.filter(paper_code = paper_code).first()
        order_items = OrderItem.objects.filter(order=order)
        ques_list = []
        for order_item in order_items:
            ques_dict = {}
            ques = order_item.question
            if not ques.for_quiz:
                continue
            ques_serializer = QuestionSerializer(ques)
            solution = Solution.objects.filter(question=ques).first()
            options = Option.objects.filter(question=ques)
            options_serializer = OptionSerializer(options, many=True)
            solution_serializer = SolutionSerializer(solution)
            ques_dict['question'] = ques_serializer.data
            ques_dict['options'] = options_serializer.data
            ques_dict['solution'] = solution_serializer.data
            ques_list.append(ques_dict)
        return Response(ques_list)
