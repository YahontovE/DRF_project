from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from education.models import Course, Lesson, Payments
from education.permissions import IsModer, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModer]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsOwner | IsModer]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner, ~IsModer]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModer]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ['date']
