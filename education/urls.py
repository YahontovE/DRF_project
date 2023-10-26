from django.template.defaulttags import url
from django.urls import path
from rest_framework.routers import DefaultRouter

from education import views
from education.apps import EducationConfig
from education.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonDestroyAPIView, LessonListAPIView, LessonUpdateAPIView, PaymentsViewSet, SubscriptionDestroyAPIView, \
    SubscriptionCreateAPIView, SubscriptionListAPIView, GetPaymentView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'payments', PaymentsViewSet, basename='payments')

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),


    path('subs/create', SubscriptionCreateAPIView.as_view(), name='create_subs'),
    path('subs/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subs_delete'),
    path('subs/', SubscriptionListAPIView.as_view(), name='subs_list'),
    path('payment/<str:payment_id>/', GetPaymentView.as_view(), name='payment_get'),

] + router.urls
