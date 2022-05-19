from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from questions.models import Question
from QuestionPaper.models import Paper
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem

from .utils import render_to_pdf 
from register_login.decorators import teacher_required

# class generatePDF(View):
#     def get(self, request, *args, **kwargs):
#         questions = Paper.objects.filter(user = request.user)
#         data = {
#             'questions':questions,
#         }
#         pdf = render_to_pdf('generatePDF.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')

@teacher_required
def generatePDF(request, order_id):
    order = Order.objects.filter(id = order_id).first()
    if order.user == request.user:
        questions = OrderItem.objects.filter(order__id = order_id)
        return render(request, 'generatePDF.html', {'order':order,'questions':questions})
    else:
        return redirect('home')