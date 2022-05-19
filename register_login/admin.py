from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User1,School,Teacher,Intern
from questions.models import Question
# Register your models here.
admin.site.register(User1,UserAdmin)
admin.site.register(School)
admin.site.register(Teacher)


 
