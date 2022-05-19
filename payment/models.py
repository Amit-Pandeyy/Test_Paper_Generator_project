from django.db import models
from register_login.models import User1
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    user = models.ForeignKey(User1 ,on_delete=models.CASCADE)   
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    paytm_status = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('RANCIKE%Y%m%d_%H%M%SODR') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.user.username + " : Rs." + str(self.amount))


class Coupon(models.Model):
    user = models.ManyToManyField(User1, blank=True)
    coupon_code = models.CharField(max_length=100)
    amount = models.IntegerField()
    def __str__(self):
        return self.coupon_code
