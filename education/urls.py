from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonDestroyAPIView, LessonListAPIView, LessonUpdateAPIView, PaymentsViewSet

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

                #Payments


] + router.urls
