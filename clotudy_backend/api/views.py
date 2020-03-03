from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from clotudy_backend.lecture.models import QuizBox, Quiz, Answer, QuizScoreRecord, LectureInformation, ClassInformation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class QuizBoxDetail(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def check_login(self, request):
        # TODO: Check if member is subscribed to the meeting
        return request.user.is_authenticated

    def get(self, request, class_pk, lecture_pk, format=None):
        if self.check_login(request):
            quiz_box = get_object_or_404(QuizBox, lecture_info=lecture_pk)
            if quiz_box.quiz_is_open:
                class_info = get_object_or_404(ClassInformation, pk=class_pk)
                quiz_set = {"category_id": quiz_box.pk, "is_open": quiz_box.quiz_is_open,
                            "category_title": quiz_box.quiz_box_title, "quiz_content": []}
                if class_info.class_instructor_id == request.user.username:
                    quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box)
                    for quiz in quiz_list:
                        answer_list = Answer.objects.filter(quiz_info=quiz)
                        quiz_set["quiz_content"].append({"id": quiz.pk, "problem": quiz.quiz_prob, "answer": [
                            {"id": answer.pk, "content": answer.answer_content} for answer in answer_list]})
                else:
                    quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box)
                    for quiz in quiz_list:
                        answer_list = Answer.objects.filter(quiz_info=quiz)
                        quiz_set["quiz_content"].append({"id": quiz.pk, "problem": quiz.quiz_prob, "answer": [
                            {"id": answer.pk, "content": answer.answer_content} for answer in answer_list]})
                return Response([quiz_set])
        return Response([])

    def post(self, request, class_pk, lecture_pk, format=None):
        if self.check_login(request):
            quiz_box = get_object_or_404(QuizBox, pk=lecture_pk)
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


class PPTTimeHistory(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            lecture = get_object_or_404(LectureInformation, pk=pk)
            times = lecture.lecture_ppt_times.split(';')
            time_list = []
            if len(times) > 0:
                for time in times:
                    time_list.append(int(time))
            return Response(time_list)
        return Response(['Please login and try again.'])

    def post(self, request, pk, format=None):
        if request.user.is_authenticated:
            lecture = get_object_or_404(LectureInformation, pk=pk)
            recv_json_data = json.loads(request.body.decode("utf-8"))
            lecture.lecture_ppt_times = recv_json_data['history']
            lecture.save()
            return Response()
        return Response(['Please login and try again.'])
