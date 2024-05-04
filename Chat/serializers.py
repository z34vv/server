from rest_framework import serializers
from .models import ChatBox, Message
from User.models import User
from Post.serializers import ImageSerializer


class MsgUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id',
                  'username',
                  'avatar']


class MessageSerializer(serializers.ModelSerializer):
    sender = MsgUserSerializer(read_only=True)
    receiver = MsgUserSerializer(read_only=True)
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Message
        fields = ['message_id',
                  'sender',
                  'receiver',
                  'content',
                  'images',
                  'is_read',
                  'created_at']


class CreateMessageSerializer(serializers.ModelSerializer):
    sender = MsgUserSerializer(read_only=True)
    receiver = MsgUserSerializer(read_only=True)
    images = ImageSerializer(many=True, required=False)

    def __init__(self, sender, receiver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender
        self.receiver = receiver

    class Meta:
        model = Message
        fields = ['message_id',
                  'sender',
                  'receiver',
                  'content',
                  'images',
                  'is_read',
                  'created_at']

    def create(self, validated_data):
        validated_data['sender'] = self.sender
        validated_data['receiver'] = self.receiver
        msg = super().create(validated_data)
        return msg
