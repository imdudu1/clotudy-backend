from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import *
import json


def lecture(request, room_id):
    class_info = ClassInformation.objects.get(pk=room_id)
    # return render(request, "lecture/{}".format(get_template_html_name(class_info.class_type)), {
    return render(request, "lecture/{}".format(_get_template_html_name(0)), {
        'room_name_json': mark_safe(json.dumps(room_id)),
        'messages': _get_user_questions_from_db(room_id),
    })


def lecture_admin(request, room_id):
    class_info = ClassInformation.objects.get(pk=room_id)

    # Quiz serializer
    recv_quiz_data = []
    quiz_box_list = QuizBox.objects.filter(lecture_info=room_id)
    for quiz_box in quiz_box_list:
        quiz_set = {"category": quiz_box.quiz_box_title, "quiz": {}}
        quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box.pk)
        for quiz in quiz_list:
            answer_list = Answer.objects.filter(quiz_info=quiz.pk)
            #quiz_set["quiz"][quiz.pk] = {"problem": quiz.quiz_prob, "answer": {{"id": answer.pk, "content": answer.answer_content, "count": answer.answer_choice_count, "is_correct": answer.answer_is_correct} for answer in answer_list}}
            quiz_set["quiz"][quiz.pk] = {"problem": quiz.quiz_prob, "answer": [{"id": answer.pk, "content": answer.answer_content, "count": answer.answer_choice_count, "is_correct": answer.answer_is_correct} for answer in answer_list]}
        recv_quiz_data.append(quiz_set)

    # return render(request, 'lecture/admin/{}'.format(get_template_html_name(class_info.class_type)), {
    return render(request, 'lecture/admin/{}'.format(_get_template_html_name(0)), {
        'room_name_json': mark_safe(json.dumps(room_id)),
        'quiz_data': recv_quiz_data,
    })


def pdf_render(request):
    return render(request, 'viewer.html', {})


def _get_user_questions_from_db(room_id):
    qna_messages = QuestionMessage.objects.filter(class_info=room_id)
    if qna_messages.exists():
        list_qna_message = [{'body': message.text, 'like-count': message.like_count, 'message-id': message.pk}
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
