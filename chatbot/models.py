
from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_user_conversation = models.BooleanField(default=False)  # Flag to identify real user conversations
    
    def __str__(self):
        return f"Conversation {self.id} - Created: {self.created_at}"

class Message(models.Model):
    ROLE_CHOICES = [
        ('User', 'User'),
        ('ChatBot', 'ChatBot'),
        ('ChatgptA', 'ChatGPT A'),
        ('ChatgptB', 'ChatGPT B'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.role}: {self.content[:30]}..."

class FoodPreference(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='food_preferences')
    food_name = models.CharField(max_length=100)
    rank = models.PositiveSmallIntegerField()  # 1, 2, 3 for top 3 preferences
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('conversation', 'rank')
        ordering = ['rank']
    
    def __str__(self):
        return f"{self.conversation.id} - Rank {self.rank}: {self.food_name}"