from django.http import Http404
from django.shortcuts import render
from clotudy_backend.lecture.models import QuizBox, Quiz, Answer
from rest_framework.views import APIView
from rest_framework.response import Response


class QuizBoxDetail(APIView):
    def get(self, request, pk, format=None):
        quiz_box = QuizBox.objects.get(lecture_info=pk)
        if quiz_box.quiz_is_open == True:
            quiz_set = {"category_id": quiz_box.pk, "is_open": quiz_box.quiz_is_open,
                        "category_title": quiz_box.quiz_box_title, "quiz_content": []}
            quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box.pk)
            for quiz in quiz_list:
                answer_list = Answer.objects.filter(quiz_info=quiz.pk)
                quiz_set["quiz_content"].append({"id": quiz.pk, "problem": quiz.quiz_prob, "answer": [
                    {"id": answer.pk, "content": answer.answer_content} for answer in answer_list]})
        return Response(quiz_set)
