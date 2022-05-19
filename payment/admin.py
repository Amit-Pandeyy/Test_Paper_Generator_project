from django.contrib import admin
from .models import Transaction, Coupon

# Register your models here.


class RegisterAdmin(admin.ModelAdmin):
    list_display = ('user','made_on','amount', 'success',)
    list_filter = ('success',)
admin.site.register(Transaction, RegisterAdmin)
admin.site.register(Coupon)
