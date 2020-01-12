from rest_framework import serializers
from .models import QuestionMessage, ClassInformation


class ClassInformationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = {
            'id',
            'class_title',
            'class_advisor',
            'class_type',
            'created_time',
        }
        model = QuestionMessage


class QuestionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = {
            'id',
            'class_info',
            'created_time',
            'question_content',
            'like_count',
        }
        model = ClassInformation
