from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from .models import *
import json


def lecture(request, class_id, lecture_id):
    # login required!!
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    try:
        class_info = ClassInformation.objects.get(pk=class_id)
        if class_info.class_instructor_id == request.user.username:
            return lecture_admin(request, class_info, lecture_id)

        lecture_info = LectureInformation.objects.get(class_info=class_info, pk=lecture_id)
        lecture_data = {"title": lecture_info.lecture_title,
                        "pdf_path": lecture_info.lecture_pdf_path,
                        "lecture_type": lecture_info.lecture_type,
                        "lecture_note": lecture_info.lecture_note}

        times = lecture_info.lecture_ppt_times.split(';')
        time_list = []
        if len(times) > 0:
            for time in times:
                time_list.append(int(time))

    except LectureInformation.DoesNotExist or ClassInformation.DoesNotExist:
        return HttpResponseRedirect("/lecture/list")
    else:
        return render(request, "lecture/{}".format(_get_template_html_name(lecture_info.lecture_type)), {
            'room_name_json': mark_safe(json.dumps(lecture_id)),
            'messages': _get_user_questions_from_db(lecture_id),
            'lecture_data': lecture_data,
            'ppt_time': time_list
        })


def lecture_admin(request, class_info, lecture_id):
    lecture_info = LectureInformation.objects.get(class_info=class_info, pk=lecture_id)
    lecture_data = {"title": lecture_info.lecture_title,
                    "pdf_path": lecture_info.lecture_pdf_path,
                    "lecture_type": lecture_info.lecture_type,
                    "lecture_note": lecture_info.lecture_note}

    # Quiz serializer
    recv_quiz_data = []
    quiz_box_list = QuizBox.objects.filter(lecture_info=lecture_info)
    for quiz_box in quiz_box_list:
        quiz_set = {"category_id": quiz_box.pk, "is_open": quiz_box.quiz_is_open,
                    "category_title": quiz_box.quiz_box_title, "quiz_content": []}
        quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box.pk)
        for quiz in quiz_list:
            solve_count = quiz.quiz_solve_count
            correct_count = quiz.quiz_correct_count
            answer_list = Answer.objects.filter(quiz_info=quiz)
            quiz_set["quiz_content"].append({"id": quiz.pk, "solve_count": solve_count, "correct_count": correct_count, "problem": quiz.quiz_prob, "answer": [
                {"id": answer.pk, "content": answer.answer_content,"choice_count_percent": (answer.answer_choice_count / solve_count) * 100, "choice_count": answer.answer_choice_count,
                 "is_correct": answer.answer_is_correct} for answer in answer_list]})
        recv_quiz_data.append(quiz_set)

    times = lecture_info.lecture_ppt_times.split(';')
    time_list = []
    if len(times) > 0:
        for time in times:
            time_list.append(int(time))

    return render(request, 'lecture/admin/{}'.format(_get_template_html_name(lecture_info.lecture_type)), {
        'room_name_json': mark_safe(json.dumps(lecture_id)),
        'quiz_data': recv_quiz_data,
        'questions': _get_user_questions_from_db(lecture_id),
        'lecture_data': lecture_data,
        'ppt_time': time_list,
    })


def pdf_render(request):
    return render(request, 'viewer.html', {})


def class_detail(request, class_id):
    try:
        class_info = ClassInformation.objects.get(pk=class_id)
        class_data = {"id": class_info.pk,
                      "title": class_info.class_title,
                      "description": class_info.class_description,
                      "thumbnail": class_info.class_thumbnail_path,
                      "created_time": class_info.class_created_time,
                      "instructor": class_info.class_instructor,
                      "instructor_id": class_info.class_instructor_id}

        lecture_info = LectureInformation.objects.filter(class_info=class_info)
        list_lecture = []
        for obj in lecture_info:
            list_lecture = [{"id": obj.pk,
                             "title": obj.lecture_title,
                             "description": obj.lecture_description}]

        return render(request, 'lecture/classDetail.html', {
            "class_data": class_data,
            "list_lecture": list_lecture,
        })
    except ClassInformation.DoesNotExist:
        return render(request, 'lecture/classDetail.html', {})


def class_list(request):
    class_info = ClassInformation.objects.all()[:10]
    list_class = []
    for obj in class_info:
        list_class.append({"id": obj.pk,
                           "title": obj.class_title,
                           "description": obj.class_description,
                           "thumbnail": obj.class_thumbnail_path,
                           "created_time": obj.class_created_time,
                           "instructor": obj.class_instructor,
                           "instructor_id": obj.class_instructor_id})

    return render(request, 'lecture/listView.html', {
        "list_class": list_class
    })


def _get_user_questions_from_db(room_id):
    qna_messages = QuestionMessage.objects.filter(lecture_info=room_id)
    if qna_messages.exists():
        list_qna_message = [{'body': message.question_content, 'likeCount': message.like_count, 'messageId': message.pk}
                            for message in qna_messages]
    else:
        list_qna_message = []
    return list_qna_message


def _get_template_html_name(class_type):
    # 0: lecture 1: participation
    if class_type == 0:
        return "lecture.html"
    elif class_type == 1:
        return "participation.html"
    elif class_type == 2:
        return "programming.html"
