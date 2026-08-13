from rest_framework import serializers

from ..models import Task
from auth_app.api.serializers import UserSerializer


class TaskDetailSerializer(serializers.ModelSerializer):
    assignee=UserSerializer(read_only=True)
    reviewer=UserSerializer(read_only=True)
    comments_count=serializers.IntegerField(
        source='comments.count',
        read_only=True,
    )

    class Meta:
        model=Task
        fields=[
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]