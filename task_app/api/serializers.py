from rest_framework import serializers

from auth_app.models import User
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



class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id=serializers.PrimaryKeyRelatedField(
        source='assignee',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    reviewer_id=serializers.PrimaryKeyRelatedField(
        source='reviewer',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        board=attrs['board']
        assignee=attrs.get('assignee')
        reviewer=attrs.get('reviewer')

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError(
                {"assignee_id": "User is not a member of this board."}
            )
        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError(
                {"reviewer_id": "User is not a member of this board."}
            )

        return attrs
    

    class Meta:
        model=Task
        fields=[
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date',
        ]



class TaskUpdateSerializer(serializers.ModelSerializer):
    assignee_id=serializers.PrimaryKeyRelatedField(
        source='assignee',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    reviewer_id=serializers.PrimaryKeyRelatedField(
        source='reviewer',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        board=self.instance.board
        assignee=attrs.get('assignee')
        reviewer=attrs.get('reviewer')

        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError(
                {"assignee_id": "User is not a mmember of this board."}
            )

        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError(
                {"reviewer_id": "User is not a member of this board."}
            )

        return attrs


    class Meta:
        model=Task
        fields=[
            'title',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date',
        ]