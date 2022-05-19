from rest_framework import serializers
from questions.models import Question, Solution, Option

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'text', 'hardness')

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('option', 'text')

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('option',)