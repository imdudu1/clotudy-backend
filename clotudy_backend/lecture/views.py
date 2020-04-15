from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
import json, uuid


def lecture(request, class_id, lecture_id):
    # login required!!
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    try:
        class_info = ClassInformation.objects.get(pk=class_id)
        if class_info.class_instructor_id == request.user.username:
            return lecture_admin(request, class_info, lecture_id)

        # 퀴즈 정보에 대한 DB 불러오기
        lecture_info = LectureInformation.objects.get(class_info=class_info, pk=lecture_id)
        lecture_data = {
            "title": lecture_info.lecture_title,
            "pdf_path": lecture_info.lecture_pdf_path,
            "lecture_type": lecture_info.lecture_type,
            "lecture_note": lecture_info.lecture_note
        }

        # 페이지별 설명한 시간을 표시하기 위한 타임라인
        times = lecture_info.lecture_ppt_times.split(';')
        time_list = []
        if len(times) > 0:
            for time in times:
                time_list.append(int(time))

        # 진행된 퀴즈 DB 불러오기
        quizboxlinks = QuizBoxLink.objects.filter(lecture_info=lecture_info)
        open_quiz_list = []
        for quizboxlink in quizboxlinks:
            if quizboxlink.quiz_is_open:
                open_quiz_list.append(quizboxlink.pk)

    except LectureInformation.DoesNotExist or ClassInformation.DoesNotExist:
        return HttpResponseRedirect("/lecture/list")
    else:
        return render(request, "lecture/{}".format(_get_template_html_name(lecture_info.lecture_type)), {
            'page_name': '수업(학생)',
            'room_name_json': mark_safe(json.dumps(lecture_id)),
            'messages': _get_user_questions_from_db(lecture_id),
            'lecture_data': lecture_data,
            'class_id': class_id,
            'ppt_time': time_list,
            'wsid': lecture_info.lecture_unique_ws_id,
            'open_quiz_list': open_quiz_list,
        })


def lecture_admin(request, class_id, lecture_id):
    lecture_info = LectureInformation.objects.get(class_info=class_id, pk=lecture_id)
    lecture_data = {
        "title": lecture_info.lecture_title,
        "pdf_path": lecture_info.lecture_pdf_path,
        "lecture_type": lecture_info.lecture_type,
        "lecture_note": lecture_info.lecture_note,
        "wsid": lecture_info.lecture_unique_ws_id
    }

    # Quiz serializer
    recv_quiz_data = []
    quiz_box_links = QuizBoxLink.objects.filter(lecture_info=lecture_info)
    for qb_link in quiz_box_links:
        #quiz_box_list = QuizBox.objects.filter(lecture_info=lecture_info)
        #for quiz_box in quiz_box_list:
        quiz_box = qb_link.quiz_box
        quiz_set = {
            "category_id": quiz_box.pk, 
            "is_open": qb_link.quiz_is_open,
            "category_title": quiz_box.quiz_box_title, 
            "quiz_content": []
        }
        quiz_list = Quiz.objects.filter(quiz_box_info=quiz_box)
        for quiz in quiz_list:
            solve_count = quiz.quiz_solve_count
            correct_count = quiz.quiz_correct_count
            answer_list = Answer.objects.filter(quiz_info=quiz)
            quiz_set["quiz_content"].append({
                "id": quiz.pk, 
                "solve_count": solve_count, 
                "correct_count": correct_count, 
                "problem": quiz.quiz_prob, 
                "answer": [{
                    "id": answer.pk, 
                    "content": answer.answer_content,
                    "choice_count_percent": (answer.answer_choice_count / solve_count) * 100 if solve_count != 0 else 0, 
                    "choice_count": answer.answer_choice_count,
                    "is_correct": answer.answer_is_correct
                } for answer in answer_list]
            })
        recv_quiz_data.append(quiz_set)

    times = lecture_info.lecture_ppt_times.split(';')
    time_list = []
    if len(times) > 0:
        for time in times:
            time_list.append(int(time))

    return render(request, 'lecture/admin/{}'.format(_get_template_html_name(lecture_info.lecture_type)), {
        'page_name': '수업 관리',
        'room_name_json': mark_safe(json.dumps(lecture_id)),
        'quiz_data': recv_quiz_data,
        'questions': _get_user_questions_from_db(lecture_id),
        'lecture_data': lecture_data,
        'class_id': class_id.pk,
        'ppt_time': time_list,
        'wsid': lecture_info.lecture_unique_ws_id,
    })


def pdf_render(request):
    return render(request, 'viewer.html', {})


def class_detail(request, class_id):
    try:
        class_info = ClassInformation.objects.get(pk=class_id)
        class_data = {
            "id": class_info.pk,
            "title": class_info.class_title,
            "description": class_info.class_description,
            "thumbnail": class_info.class_thumbnail_path,
            "created_time": class_info.class_created_time,
            "instructor": class_info.class_instructor,
            "instructor_id": class_info.class_instructor_id
        }

        lecture_info = LectureInformation.objects.filter(class_info=class_info)
        list_lecture = []
        for obj in lecture_info:
            list_lecture.append({
                "id": obj.pk,
                "title": obj.lecture_title,
                "description": obj.lecture_description
            })

        return render(request, 'lecture/class_detail.html', {
            'page_name': '수업 내용',
            "class_data": class_data,
            "list_lecture": list_lecture,
        })
    except ClassInformation.DoesNotExist:
        return render(request, 'lecture/class_detail.html', {})


def class_list(request):
    class_info = ClassInformation.objects.all()[:10]
    list_class = []
    for obj in class_info:
        list_class.append({
            "id": obj.pk,
            "title": obj.class_title,
            "description": obj.class_description,
            "thumbnail": obj.class_thumbnail_path,
            "created_time": obj.class_created_time,
            "instructor": obj.class_instructor,
            "instructor_id": obj.class_instructor_id
        })

    return render(request, 'lecture/class_list.html', {
        'page_name': '강의 목록',
        "list_class": list_class
    })


def _get_user_questions_from_db(room_id):
    qna_messages = QuestionMessage.objects.filter(lecture_info=room_id)
    if qna_messages.exists():
        list_qna_message = [{
            'body': message.question_content, 
            'likeCount': message.like_count, 
            'messageId': message.pk, 
            'userID': message.user_id
        } for message in qna_messages]
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


'''
JSON example
{
    'title': '',
    'description': '',
    'instructor_name': '',
    'thumbnail_path': ''
}
'''
@csrf_exempt
def class_create(request):
    # login required!!
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    if request.method == "POST":
        req_data = json.loads(request.body)
        title = req_data['title']
        description = req_data['description']
        instructor_name = req_data['instructor_name']
        thumbnail_path = req_data['thumbnail_path']
        username = request.user.username
        new_class = ClassInformation.objects.create(
            class_title=title,
            class_description=description,
            class_instructor_id=username,
            class_instructor=instructor_name,
            class_thumbnail_path=thumbnail_path
        )
        return HttpResponse("*^^*")
    elif request.method == "GET":
        username = request.user.username
        class_list = ClassInformation.objects.filter(class_instructor_id=username)
        class_res_data = []
        for class_obj in class_list:
            class_res_data.append({
                'id': class_obj.pk,
                'title': class_obj.class_title,
                'description': class_obj.class_description,
                'thumbnail': class_obj.class_thumbnail_path,
                'date': class_obj.class_created_time,
            })
        return render(request, "lecture/class/create.html", {
            'page_name': '강의 생성',
            'class_list': class_res_data
        })


'''
JSON example
{
    'title': 'quiz title',
    'quizs': [
        {
            'content': 'quiz content',
            'answers': [
                {
                    'content': '(A) 12.18',
                    'is_correct': false or true,
                },
                {
                    'content': '(B) 12.06',
                    'is_correct': false or true,
                }
            ]
        },
        {
            'content': 'quiz content',
            'answers': [
                {
                    'content': '(A) 12.12',
                    'is_correct': false or true,
                }
            ]
        }
    ]
}
'''
@csrf_exempt
def quiz_create(request):
    # login required!!
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    if request.method == "POST":
        req_data = json.loads(request.body)
        title=req_data['title']
        new_quiz_box = QuizBox.objects.create(
            quiz_box_title=title,
            quiz_box_owner=request.user.username,
        )

        quizs = req_data['quizs']
        for quiz in quizs:
            new_quiz = Quiz.objects.create(
                quiz_box_info=new_quiz_box,
                quiz_prob=quiz['content'],
                quiz_item_num=len(quiz['answers']),
            )
            answers = quiz['answers']
            for answer in answers:
                Answer.objects.create(
                    quiz_info=new_quiz,
                    answer_is_correct=answer['is_correct'],
                    answer_content=answer['content'],
                )
        return HttpResponse("*^^*")
    elif request.method == "GET":
        return render(request, "lecture/quiz/create.html", {})


'''
JSON example
{
    'class_id': 1,
    'title': 'C언어 프로그래밍',
    'description': '',
    'type': 0,
    'pdf': '',
    'note': '',
    'quizboxs': [1, 2, ...]
}
'''
@csrf_exempt
def lecture_create(request, cid):
    # login required!!
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    class_info = ClassInformation.objects.get(pk=cid)
    if class_info.class_instructor_id != request.user.username:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        req_data = json.loads(request.body)
        ws_id = str(uuid.uuid4()).split('-')
        ws_id = '{}{}{}{}'.format(ws_id[0], ws_id[1], ws_id[2], ws_id[3])
        new_lecture = LectureInformation.objects.create(
            class_info=class_info,
            lecture_title=req_data['title'],
            lecture_description=req_data['description'],
            lecture_type=req_data['type'],
            lecture_pdf_path=req_data['pdf'],
            lecture_note=req_data['note'],
            lecture_unique_ws_id=ws_id,
        )
        quizboxs = req_data['quizboxs']
        for quizbox in quizboxs:
            try:
                qb = QuizBox.objects.get(pk=quizbox)
                QuizBoxLink.objects.create(
                    lecture_info=new_lecture,
                    quiz_box=qb,
                )
            except QuizBox.DoesNotExist:
                continue
        return HttpResponse("*^^*")
    elif request.method == "GET":
        username = request.user.username
        quizbox_list = QuizBox.objects.filter(quiz_box_owner=username)
        quizbox_res_data = []
        for quizbox_obj in quizbox_list:
            quizbox_res_data.append({
                'id': quizbox_obj.pk,
                'title': quizbox_obj.quiz_box_title,
            })
        return render(request, "lecture/lecture/create.html", {
            'page_name': '수업 생성',
            'cid': class_info.pk,
            'quizbox_list': quizbox_res_data
        })
