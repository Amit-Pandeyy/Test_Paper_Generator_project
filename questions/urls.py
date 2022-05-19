from django.urls import path, include
from .views import question_list, select_class,select_subject,question_list,select_chapter,question_topic_selector, search_questions


urlpatterns = [
   path('chaining', include('smart_selects.urls')),
   path('select_class/',select_class,name="select_class" ),
   path('select_subject/standard:<str:standard_name>',select_subject,name="select_subject"),
   path('question_list/standard:<str:standard_name>/subject:<str:subject_name>/chapter:<str:chapter_name>/<int:chapter_id>',question_list,name="question_list"),
   path('select_chapter/standard:<str:standard_name>/subject:<str:subject_name>/',select_chapter,name="select_chapter"),
   path('question_topic_selector',question_topic_selector,name="question_topic_selector"),
   path('search_questions/<int:chapter_id>/', search_questions, name = 'search_questions')

]
