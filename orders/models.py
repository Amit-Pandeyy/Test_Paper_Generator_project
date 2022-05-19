from django.db import models
from register_login.models import User1
from questions.models import Question
from django.utils import timezone
from tinymce.models import HTMLField 
# Create your models here.



class Order(models.Model):
    user = models.ForeignKey(User1,on_delete = models.CASCADE)   
    test_name = models.CharField(max_length=255)
    institute_name = models.CharField(max_length=255)
    paper_code = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    guidelines = HTMLField()
    created_at =  models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    total_marks = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return str(self.created_at)+"Name:"+str(self.test_name)
    def get_total_marks(self):
        return sum(item.marks for item in self.items.all())
    def get_total_cost(self):
        return sum(item.price for item in items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items",on_delete=models.CASCADE,default="")
    question = models.ForeignKey(Question,related_name="order_items",on_delete=models.CASCADE,default=None)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    marks = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default = 0)

    def __str__(self):
        return '{}'.format(self.id)
    
    