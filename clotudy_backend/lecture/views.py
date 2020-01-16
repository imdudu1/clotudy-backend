from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import QuestionMessage, ClassInformation
import json


def lecture(request, room_id):
    class_info = ClassInformation.objects.get(pk=room_id)
    return render(request, "lecture/{}".format(get_template_html_name(class_info.class_type)), {
        'room_name_json': mark_safe(json.dumps(room_id)),
        'messages': get_user_questions_from_db(room_id),
    })


def lecture_admin(request, room_id):
    class_info = ClassInformation.objects.get(pk=room_id)
    return render(request, 'lecture/admin/{}'.format(get_template_html_name(class_info.class_type)), {
        'room_name_json': mark_safe(json.dumps(room_id))
    })


def pdf_render(request):
    return render(request, 'viewer.html', {})


def get_user_questions_from_db(room_id):
    qna_messages = QuestionMessage.objects.filter(lecture=room_id)
    if qna_messages.exists():
        list_qna_message = [{'body': message.text, 'like-count': message.like_count, 'message-id': message.pk}
                            for message in qna_messages]
    else:
        list_qna_message = []

    return list_qna_message


def get_template_html_name(class_type):
    # 0: lecture 1: participation
    if class_type == 0:
        return "lecture.html"
    elif class_type == 1:
        return "participation.html"
