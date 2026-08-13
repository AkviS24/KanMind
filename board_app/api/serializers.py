from rest_framework import serializers

from ..models import Board
from auth_app.api.serializers import UserSerializer
from task_app.api.serializers import TaskDetailSerializer


class BoardSerializer(serializers.ModelSerializer):
    owner_id=serializers.IntegerField(
        source="owner.id",
        read_only=True,
    )
    member_count=serializers.IntegerField(
        source="members.count",
        read_only=True,
    )
    ticket_count=serializers.IntegerField(
        source="tasks.count",
        read_only=True,
    )

    tasks_to_do_count=serializers.SerializerMethodField()
    tasks_high_prio_count=serializers.SerializerMethodField()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()

    class Meta:
        model=Board
        fields=[
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]



class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id=serializers.IntegerField(source='owner.id', read_only=True,)
    members=UserSerializer(many=True, read_only=True,)
    tasks=TaskDetailSerializer(many=True, read_only=True,)

    class Meta:
        model=Board
        fields=[
            'id',
            'title',
            'owner_id',
            'members',
            'tasks',
        ]



class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Board
        fields=[
            'title',
            'members',
        ]