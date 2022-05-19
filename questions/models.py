from django.db import models
from django.db.models.enums import TextChoices
from tinymce.models import HTMLField 
from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey
from django.utils import timezone
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
# import mathfield
# Create your models here.

HARDNESS_CHOICES = (
    ('basic','basic'),
    ('easy','easy'),
    ('medium','medium'),
    ('hard','hard'),
)

STATUS_CHOICES = (
    ("No","No"),
    ("Yes","Yes"),
)


class Standard(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to="standard")

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to="subjects")
    standard = models.ForeignKey(Standard,related_name="subject",on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to="chapters")
    standard = models.ForeignKey(Standard,related_name="chapter",on_delete=models.CASCADE)
    subject = ChainedForeignKey(Subject, chained_field='standard',chained_model_field="standard",show_all=False,auto_choose=True,sort=True,related_name="chapter",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Topic(models.Model):
    name = models.CharField(max_length=500)
    standard = models.ForeignKey(Standard,related_name="standard",on_delete=models.CASCADE)
    subject = ChainedForeignKey(Subject, chained_field='standard',chained_model_field="standard",show_all=False,auto_choose=True,sort=True,related_name="topic",on_delete=models.CASCADE)
    chapter = ChainedForeignKey(Chapter, chained_field='subject',chained_model_field="subject",show_all=False,auto_choose=True,sort=True,related_name="topic",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,default=get_current_authenticated_user)
    title = models.CharField(max_length=500)
    text = HTMLField()
    hardness = models.CharField(max_length=100,choices=HARDNESS_CHOICES)
    topic = models.ManyToManyField(Topic,related_name="Question",blank=True)
    marks = models.IntegerField(default=0)
    standard = models.ForeignKey(Standard,related_name="Question",on_delete=models.CASCADE)
    subject = ChainedForeignKey(Subject, chained_field='standard',chained_model_field="standard",show_all=False,auto_choose=True,sort=True,related_name="Question",on_delete=models.CASCADE)
    chapter = ChainedForeignKey(Chapter, chained_field='subject',chained_model_field="subject",show_all=False,auto_choose=True,sort=True,related_name="Question",on_delete=models.CASCADE)
    topic  = ChainedForeignKey(Topic, chained_field='chapter',chained_model_field="chapter",show_all=False,auto_choose=True,sort=True,related_name="Question",on_delete=models.CASCADE)
    status = models.CharField(max_length=500,default="Yes",blank=True,null=True)
    # for_quiz = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Option(models.Model):
    option = HTMLField()
    question = models.ForeignKey(Question,related_name="Option",on_delete=models.CASCADE)
    def __str__(self):
        return self.question.title


OPTION_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
)

class OptionNumber(models.Model):
    option = models.CharField(max_length=100,choices=OPTION_CHOICES)
    def __str__(self):
        return self.option

class Solution(models.Model):
    question = models.OneToOneField(Question,on_delete=models.CASCADE, related_name='solution')
    option = models.ManyToManyField(OptionNumber,related_name="Solution",blank=True)
    text = HTMLField()

    def __str__(self):
        return self.question.title