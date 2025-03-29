from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ConversationSerializer
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import OpenAIService
from .models import Conversation, Message
from rest_framework.views import APIView


class GenerateConversationView(APIView):
    """Simulate conversations between ChatGPT A and B"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        count = int(request.data.get('count', 1))  # Default to 1 conversation
        service = OpenAIService()
        results = []
        convo_id = []

        for _ in range(count):
            question = service.ask_favorite_foods()
            preferences = service.generate_food_preferences(question)

            # Append the conversation ID to the list
            convo_id.append(preferences['conversation_id'])
        
        convo_objs = Conversation.objects.filter(id__in=convo_id)
        serializer = ConversationSerializer(convo_objs, many=True)
        return Response(serializer.data)




openai_service = OpenAIService()

def conversations_list(request):
    """Show a list of all conversations"""
    conversations = Conversation.objects.all().order_by('-created_at')  # Assuming you have a created_at field
    return render(request, 'conversations_list.html', {'conversations': conversations})

# View for the chat interface page
def chat_interface(request):
    """Render the chat interface"""
    return render(request, 'chat.html')

# API endpoint to start a new conversation
@csrf_exempt
@require_http_methods(["POST"])
def start_conversation(request):
    """Create a new conversation and return the initial bot message"""
    result = openai_service.create_user_conversation()
    return JsonResponse(result)

# API endpoint to send a message and get a response
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Process a user message and return the bot's response"""
    try:
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        user_message = data.get('message')
        
        if not conversation_id or not user_message:
            return JsonResponse({"error": "Missing conversation_id or message"}, status=400)
        
        result = openai_service.chat_with_user(conversation_id, user_message)
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

# View to display conversation history
def conversation_history(request, conversation_id):
    """Show the full history of a conversation"""
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        messages = Message.objects.filter(conversation=conversation).order_by('created_at')
        
        food_preferences = conversation.food_preferences.all().order_by('rank')
        
        context = {
            'conversation': conversation,
            'messages': messages,
            'food_preferences': food_preferences
        }
        
        return render(request, 'history.html', context) 
    
    except Conversation.DoesNotExist:
        return render(request, 'error.html', {'error': 'Conversation not found'})