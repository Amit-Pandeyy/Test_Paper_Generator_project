import os
import random
import string
from django import forms
from django.shortcuts import redirect, render
from .forms import UploadQuestionByTextForm
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from register_login.decorators import teacher_required
from QuestionPaper.models import Paper

# Create your views here.

@login_required
@teacher_required
def upload_question(request):
    if request.method=='POST':
        form = UploadQuestionByTextForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            question=form.save()
            Paper(user=request.user, question=question, marks = question.marks).save()
            messages.success(request, 'Question uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Some Error Occured!')
    else:
        form = UploadQuestionByTextForm()
    return render(request, 'upload_question.html',{'form':form})

@login_required
@teacher_required
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)
        
        N = 10
        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        file_name = str(file_name)+'.'+file_name_suffix


        file_path = os.path.join(path, file_name)

        file_url = f'{settings.BASE_URL}{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})