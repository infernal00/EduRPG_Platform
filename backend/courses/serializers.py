from rest_framework import serializers

from .models import Lesson, Subject, Topic


class LessonSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source="topic.subject.id", read_only=True)
    subject_name = serializers.CharField(source="topic.subject.name", read_only=True)
    topic_id = serializers.IntegerField(source="topic.id", read_only=True)
    topic_title = serializers.CharField(source="topic.title", read_only=True)
    topic = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content",
            "level",
            "xp_reward",
            "coins_reward",
            "order",
            "is_active",
            "topic_id",
            "topic_title",
            "subject_id",
            "subject_name",
            "topic",
            "subject",
        ]

    def get_topic(self, lesson):
        return {
            "id": lesson.topic_id,
            "title": lesson.topic.title,
        }

    def get_subject(self, lesson):
        subject = lesson.topic.subject
        return {
            "id": subject.id,
            "name": subject.name,
            "icon": subject.icon,
        }


class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "title",
            "description",
            "order",
            "lessons",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "description",
            "icon",
            "is_active",
            "created_at",
            "topics",
        ]
