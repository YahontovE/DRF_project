from rest_framework import serializers

from education.models import Lesson, Course, Payments, Subscription
from education.validators import Video_linkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [Video_linkValidator(field='video_link')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lessons', many=True, read_only=True)
    #activ = SubscriptionSerializer(source='subs', many=True, read_only=True)
    activ=serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.get('context').get('request')
    @staticmethod
    def get_lessons_count(instance):
        return instance.lessons.count()

    def get_activ(self,instance):
        activ = Subscription.objects.filter(user=self.request.user, course=instance).first()
        if activ and activ.is_activ:
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

# class SubscriptionSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model=Subscription
#         fields='__all__'
