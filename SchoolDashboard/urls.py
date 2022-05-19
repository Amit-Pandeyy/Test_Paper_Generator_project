from django.urls import path
from .views import add_teacher,show_teachers,increase_credits


urlpatterns = [
   path('',show_teachers,name="school_dashboard" ),
   path('add_teacher/',add_teacher,name="add_teacher" ),
   path('increase_credits/',increase_credits, name='increase_credits'),

]
