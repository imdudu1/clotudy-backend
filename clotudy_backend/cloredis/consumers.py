# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from clotudy_backend.lecture.models import QuestionMessage, ClassInformation, LectureInformation, QuizBox
import json


class Consumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

    async def connect(self):
        # Login required!!
        if not self.scope['user'].is_authenticated:
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Login required!!
        if not self.scope['user'].is_authenticated:
            return

        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        data = text_data_json['data']

        if action == 'live-qna-chat':
            msg_pk = await self.save_qna_message(data)
            data['messageId'] = msg_pk
            data['userID'] = self.scope['user'].username
        elif action == 'add-like-count':
            await self.add_like_count(data)
        elif action == 'show-quiz-modal':
            await self.set_quiz_box(data)
        """
        elif action == 'sync-ppt-page':
            sender_name = self.scope['user'].username
            # VULNERABILITY
            is_owner = await self.check_class_owner(sender_name, data['class_id'])
            if not is_owner:
                return
        """

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'action': action,
                'data': data,
            }
        )

    async def chat_message(self, event):
        if 'action' in event and 'data' in event:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'action': event['action'],
                'data': event['data'],
            }))

    @database_sync_to_async
    def save_qna_message(self, data):
        try:
            lecture = LectureInformation.objects.get(pk=data['lecture'])
        except ClassInformation.DoesNotExist:
            return -1
        else:
            return QuestionMessage.objects.create(
                question_content=data['qna']['body'],
                user_id=self.scope['user'].username,
                lecture_info=lecture,
            ).pk;

    @database_sync_to_async
    def add_like_count(self, data):
        try:
            lecture = ClassInformation.objects.get(pk=data['lecture'])
            message = QuestionMessage.objects.get(lecture=lecture, pk=data['messageId'])
        except ClassInformation.DoesNotExist or QuestionMessage.DoesNotExist:
            return
        else:
            message.like_count += 1
            message.save()

    @database_sync_to_async
    def check_class_owner(self, user_name, class_id):
        instructor_id = ClassInformation.objects.get(pk=class_id).class_instructor_id
        if user_name == instructor_id:
            return True
        return False

    @database_sync_to_async
    def set_quiz_box(self, data):
        box = QuizBox.objects.get(pk=data['quizBoxId'])
        if box.quiz_is_open == False:
            box.quiz_is_open = True
        else:
            box.quiz_is_open = False
        box.save()
