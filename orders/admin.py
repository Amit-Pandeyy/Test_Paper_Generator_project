from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    fields =["user",'test_name',"institute_name","paper_code","subject_code","description","created_at"]
    list_display = ["user",'test_name',"institute_name","paper_code","subject_code","description","created_at"]
    inlines = [OrderItemInline]
    search_fields = ("test_name","institute_name","paper_code","subject_code","description")


admin.site.register(Order,OrderAdmin)