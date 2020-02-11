from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from clotudy_backend.lecture.models import QuizBox, Quiz, Answer, QuizScoreRecord
from rest_framework.views import APIView
from rest_framework.response import Response


class QuizBoxDetail(APIView):

    def check_login(self, request):
        # TODO: Check if member is subscribed to the meeting
        return request.user.is_authenticated

    def get(self, request, pk, format=None):
        if self.check_login(request):
            quiz_box = get_object_or_404(QuizBox, lecture_info=pk)
            if quiz_box.quiz_is_open:
                quiz_set = {"category_id": quiz_box.pk, "is_open": quiz_box.quiz_is_open,
                            "category_title": quiz_box.quiz_box_title, "quiz_content": []}
                quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box)
                for quiz in quiz_list:
                    answer_list = Answer.objects.filter(quiz_info=quiz)
                    quiz_set["quiz_content"].append({"id": quiz.pk, "problem": quiz.quiz_prob, "answer": [
                        {"id": answer.pk, "content": answer.answer_content} for answer in answer_list]})
                return Response([quiz_set])
        return Response([])

    def post(self, request, pk, format=None):
        if self.check_login(request):
            quiz_box = get_object_or_404(QuizBox, pk=pk)
            if quiz_box.quiz_is_open:
                try:
                    record = QuizScoreRecord.objects.get(quiz_box_info=quiz_box, user_id=request.user.username)
                    return Response(['You have already been taken.'])
                except QuizScoreRecord.DoesNotExist:
                    total_score = 0
                    for key in request.data:
                        if key != "csrfmiddlewaretoken":
                            qz = Quiz.objects.get(pk=key, quiz_box_info=quiz_box)
                            qz.quiz_solve_count += 1
                            ans = Answer.objects.get(quiz_info=qz, pk=request.data[key])
                            ans.answer_choice_count += 1
                            if ans.answer_is_correct:
                                total_score = total_score + qz.quiz_score
                                qz.quiz_correct_count += 1
                                quiz_box.save()
                            ans.save()
                            qz.save()
                    QuizScoreRecord.objects.create(lecture_info=quiz_box.lecture_info, quiz_box_info=quiz_box,
                                                   user_id=request.user.username, score=total_score)
                    return Response(total_score)
            return Response(['This quiz is not open yet.'])
        return Response(['Please login and try again.'])
