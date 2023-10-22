from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Lesson, Course, Subscription
from users.models import User


class lessonTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "title": "test",
            "description": "test",
            "video_link": "https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s",
        }

    def test_get_list(self):
        """Тест вывода уроков"""
        Lesson.objects.create(id=1, title='test', description='test', image=None,
                              video_link='https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s', user=None, course=None)
        response = self.client.get(
            reverse('education:lesson_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': 1, 'title': 'test', 'description': 'test', 'image': None,
             'video_link': 'https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s', 'user': None, 'course': None}]}
                         )

    def test_create_lesson(self):
        """тест создания урока"""

        url = reverse("education:create_lesson")
        response = self.client.post(url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(), {"id": 1,
                                           "title": "test",
                                           "description": "test",
                                           "image": None,
                                           "video_link": "https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s",
                                           "user": None,
                                           "course": None})

    def test_update_lessons(self):
        """тест редактирования урока"""
        Lesson.objects.create(id=1, title='no test', description='test', image=None,
                              video_link='https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s', user=None, course=None)

        url = reverse("education:lesson_update", kwargs={"pk": 1})
        response = self.client.put(url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {'id': 1, 'title': 'test', 'description': 'test', 'image': None,
                                           'video_link': 'https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s', 'user': None,
                                           'course': None}
                         )

    def test_delete_lessons(self):
        """тест удаления урока"""

        Lesson.objects.create(id=1, title='no test', description='test', image=None,
                              video_link='https://www.youtube.com/watch?v=_x8DV1WLtks&t=142s', user=None, course=None)

        url = reverse("education:lesson_delete", kwargs={"pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test',
            description='Test'
        )

    def test_subscription_create(self):
        """Тест создания подписки"""
        self.client.force_authenticate(user=self.user)

        data = {
            'user': self.user.id,
            'course': self.course.id,
            'is_activ': True
        }

        response = self.client.post(
            reverse('education:create_subs'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        self.client.force_authenticate(user=self.user)

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_activ='True'
        )

        response = self.client.delete(
            reverse('course:subscription_delete',
                    args=[self.subscription.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)