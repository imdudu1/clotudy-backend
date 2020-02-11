from rest_framework import serializers
from clotudy_backend.lecture.models import QuizBox, Quiz, Answer


class QuizBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizBox
        fields = ('quiz_box_title', 'quiz_is_open')
