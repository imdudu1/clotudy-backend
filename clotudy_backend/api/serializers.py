from rest_framework import serializers
from .models import QuestionMessage, ClassInformation


class ClassInformationLCSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'class_title',
            'class_advisor',
            'class_explain',
            'class_type',
            'created_time',
        ]
        model = ClassInformation


class ClassInformationRUDSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'class_title',
            'class_advisor',
            'class_explain',
            'class_type',
            'created_time',
            'class_invite_code',
        ]
        model = ClassInformation


class QuestionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'class_info',
            'created_time',
            'question_content',
            'like_count',
        ]
        model = QuestionMessage
