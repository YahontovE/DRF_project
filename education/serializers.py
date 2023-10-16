from rest_framework import serializers

from education.models import Lesson, Course, Payments


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # read_only=True source='lesson_set'
    lessons_count = serializers.SerializerMethodField()
    # lesson = LessonSerializer(many=True, read_only=True)
    lesson = LessonSerializer(source='lessons', many=True, read_only=True)

    @staticmethod
    def get_lessons_count(instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
