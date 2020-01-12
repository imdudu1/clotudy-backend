from django.shortcuts import render
from rest_framework import generics

from .serializers import QuestionMessageSerializer, ClassInformationLCSerializer, ClassInformationRUDSerializer
from .models import QuestionMessage, ClassInformation


class ListClass(generics.ListCreateAPIView):
    queryset = ClassInformation.objects.all()
    serializer_class = ClassInformationLCSerializer


class DetailClass(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassInformation.objects.all()
    serializer_class = ClassInformationRUDSerializer


class ListQuestionMessage(generics.ListCreateAPIView):
    queryset = QuestionMessage.objects.all()
    serializer_class = QuestionMessageSerializer
