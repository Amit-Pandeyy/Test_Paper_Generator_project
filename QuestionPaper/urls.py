from django.urls import path
from . import views
from questions.views import get_question


urlpatterns = [
    path('', views.show_paper, name = 'paper'),
    path('add_to_paper/', views.add_to_paper, name='add_to_paper'),
    path('remove_paper/', views.remove_paper, name='remove_paper'),
    path('increase_marks/', views.increase_marks, name='increase_marks'),
    path('decrease_marks/', views.decrease_marks, name='decrease_marks'),
    path('get_question/', get_question, name='get_question'),
    path('get_quiz/<str:paper_code>', views.get_quiz.as_view(), name='get_quiz'),
]