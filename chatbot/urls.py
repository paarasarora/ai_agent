from django.urls import path
from . import views
from .views import  GenerateConversationView

app_name = "chatbot"

 
urlpatterns = [
    
    # New chatbot endpoints
    path('chat/invoke', views.chat_interface, name='chat_interface'),
    path('start/', views.start_conversation, name='start_conversation'),
    path('message/', views.send_message, name='send_message'),
    path('history/<int:conversation_id>/', views.conversation_history, name='conversation_history'),
    path('generate/', GenerateConversationView.as_view(), name='generate-conversation'),
    path('', views.conversations_list, name='conversations_list'),
]