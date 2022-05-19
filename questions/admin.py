from django.contrib import admin
from django.forms.models import model_to_dict
from .models import Solution, Option
from register_login.models import  User1
# Register your models here.
from .models import Standard,Subject,Chapter,Topic,Question,Option,Solution


class OptionAdmin(admin.StackedInline):
    model = Option
class SolutionAdmin(admin.StackedInline): 
    model = Solution
    
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields=('user','status',)
    search_fields =('id','title','user__username','user__email')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super(QuestionAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
    opAdmin = OptionAdmin
    opAdmin.min_num=4
    opAdmin.extra = 0
    inlines = [opAdmin, SolutionAdmin]
    class Meta:
       model = Question

class TopicAdmin(admin.ModelAdmin):
    search_fields =('name','standard__name','chapter__name')
    class Meta:
        model = Topic
class ChapterAdmin(admin.ModelAdmin):
    search_fields = ('name','standard__name','subject__name')
    class Meta:
        model = Chapter


class StandardAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    class Meta:
        model = Standard

class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('name','standard__name')
    class Meta:
        model = Subject

admin.site.register(Standard,StandardAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Option)
admin.site.register(Solution)
admin.site.register(Question,QuestionAdmin)
