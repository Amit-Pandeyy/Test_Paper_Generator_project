from django.db import models
from django.conf import settings
from questions.models import Question

class Paper(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    marks = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username + " : " + self.question.title)