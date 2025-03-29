from rest_framework import serializers
from .models import Conversation,FoodPreference,Message

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodPreference
        fields = ['food_name', 'rank']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'role', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    food_preferences = PreferenceSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'is_vegetarian', 'is_vegan', 'created_at', 'food_preferences', 'messages']
