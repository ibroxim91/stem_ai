from rest_framework import serializers
from apps.chat.models import UserChat, UserOpenAIChatHistory
from apps.main.serializers.question_group_serializer import QuestionGroupSerializer
from apps.main.serializers.question_serializer import QuestionSerializer


class UserOpenAIChatHistorySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    total_cost_usd = serializers.CharField(source='cost_usd')
    class Meta:
        model = UserOpenAIChatHistory
        fields = [
            'id', 'model_name', 'prompt_tokens', 'completion_tokens', 
            'total_tokens', 'total_cost_usd', "questions",  'response_text', 
            'created_at'
        ]

    def get_questions(self, obj):
        language = self.context.get('language')
        data = []
        for question in obj.questions.all():
            result = {
                "question_group": QuestionGroupSerializer(question.question_group, many=False).data,
                "question": QuestionSerializer(question.question, many=False).data,
                "boolean_answer": question.boolean,
                "options": [option.id for option in question.question_options.all()]
            }  
            data.append(result) 
        return data


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['id', 'title', 'description', 'message_count', 'created_at']


class UserChatDetailSerializer(serializers.ModelSerializer):
    messages = UserOpenAIChatHistorySerializer(many=True, read_only=True, source="chats")

    class Meta:
        model = UserChat
        fields = [
            'id', 'title', 'description', 'message_count', 'created_at', 'messages'
        ]
