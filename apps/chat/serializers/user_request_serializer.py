from rest_framework import serializers

class QuestionAnswerSerializer(serializers.Serializer):
    question_group = serializers.IntegerField()
    question_id = serializers.IntegerField()
    boolean_answer = serializers.BooleanField(required=False, allow_null=True)
    free_answer = serializers.CharField(required=False, allow_null=True)
    options = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

class UserRequestSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    language_id = serializers.IntegerField(required=False, allow_null=True)
    chat_id = serializers.IntegerField(required=False, allow_null=True)
    questions = QuestionAnswerSerializer(many=True)

    def create(self, validated_data):
        
        return validated_data


class UserResponseChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text='Chat ID')
    title = serializers.CharField(help_text='Chat title')
    created_at = serializers.DateTimeField(help_text='Chat creation date')
    message_id = serializers.IntegerField(help_text='Message ID')

class UserResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    prompt_tokens = serializers.IntegerField(required=False, allow_null=True)
    completion_tokens = serializers.IntegerField(required=False, allow_null=True)
    total_tokens = serializers.IntegerField(required=False, allow_null=True)
    total_cost_usd = serializers.IntegerField(required=False, allow_null=True)
    chat = UserResponseChatSerializer(many=False)

