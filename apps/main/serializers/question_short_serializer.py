from rest_framework import serializers
from apps.main.models import Question
from apps.main.models.question_group import QuestionGroup



class QuestionSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = Question
        fields = [
            'id', 'group', 'type'
        ]