from django.urls import path, include
from .views import upload_question, upload_image

urlpatterns = [
    path('', upload_question, name='upload_question'),
    path('upload_image/', upload_image),
]