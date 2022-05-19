from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save,Signal
from questions.models import Question
class User1(AbstractUser):
    is_school = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=20, blank=True)
    credit = models.IntegerField(default=0)

class Activation(models.Model):
    user = models.ForeignKey(User1, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


class Teacher(models.Model):
    user = models.OneToOneField(User1, on_delete = models.CASCADE, primary_key = True)
    email = models.EmailField
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class School(models.Model):
    user = models.OneToOneField(User1, on_delete = models.CASCADE, primary_key = True)
    email = models.EmailField
    school_name = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    teachers= models.ManyToManyField(Teacher)    

class Intern(models.Model):
    user = models.OneToOneField(User1, on_delete=models.CASCADE,primary_key = True)
    no_of_questions = models.IntegerField(default=0)
    paid_for = models.IntegerField(default=0)
    amount_left = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


def assign_intern(sender,instance,created,**kwargs):
    
    if created:
        intern = Intern.objects.filter(user = instance.user).first()
        if intern is not None:
            intern.no_of_questions += 1
            intern.amount_left += 1 
            intern.save()

post_save.connect(assign_intern,Question)