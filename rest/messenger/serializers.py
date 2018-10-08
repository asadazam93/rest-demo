from django.contrib.auth.models import User
from rest.messenger.models import Message
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'sender', 'sender_name', 'receiver', 'receiver_name')

    sender_name = serializers.SerializerMethodField('get_senders_name')
    receiver_name = serializers.SerializerMethodField('get_receivers_name')

    def get_senders_name(self, obj):
        """

        Args:
            obj:

        Returns:
            Returns username of the sender
        """
        return obj.sender.username

    def get_receivers_name(self, obj):
        """

        Args:
            obj:

        Returns:
            Returns username of the receiver
        """
        return obj.receiver.username
