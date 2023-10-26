from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import SECRET_KEY_STRIPE
from education.models import Course, Lesson, Payments, Subscription
from education.paginators import LessonPaginator, CoursePaginator
from education.permissions import IsModer, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
import stripe


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

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
    permission_classes = [AllowAny,~IsModer]

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
    permission_classes = [IsAuthenticated | IsModer] # IsAuthenticated
    pagination_class = LessonPaginator


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    #filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ['date']

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        payment.save()
        return super().perform_create(serializer)


    def payment_create(self):
        if self.action == 'create':
            stripe.api_key = 'sk_test_51O5BP8HzMiqB6nM069g2B0lGlWOfGueOBi4XPZTqICzTLGmqOBaL7oUjrUrJNOBSs4sTrZhuGa4VEe1T5F9vlGTK00LgpSWZG1'

            pay=stripe.PaymentIntent.create(
                amount=self.request.payment_sum,
                currency="usd",
                automatic_payment_methods={"enabled": True},
                course=self.request.course,
                user=self.request.user,

            )
            print(pay.client_secret)
            pay.save()
            return Response(status=status.HTTP_200_OK, data=pay)

class GetPaymentView(APIView):
    def get_view_name(self,request,payment_id):
        stripe.api_key = 'sk_test_51O5BP8HzMiqB6nM069g2B0lGlWOfGueOBi4XPZTqICzTLGmqOBaL7oUjrUrJNOBSs4sTrZhuGa4VEe1T5F9vlGTK00LgpSWZG1'
        payment_intent=stripe.PaymentIntent.retrieve(payment_id)
        payment_intent.save()
        return Response({
            'status': payment_intent.status, })

    # def get(self, request, payment_id):
    #     payment_intent = stripe.PaymentIntent.retrieve(payment_id)
    #     return Response({
    #         'status': payment_intent.status, })

class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [AllowAny]

class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [AllowAny]
