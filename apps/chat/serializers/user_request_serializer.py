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