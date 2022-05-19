from questions.models import Question, Standard, Subject, Chapter, Topic
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from django import forms

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class UploadQuestionByTextForm(ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = Question
        exclude = ('user',)
