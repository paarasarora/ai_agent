import os
import openai
import json
import random
from .models import Conversation, FoodPreference, Message
from django.conf import settings


OPEN_AI_KEY = settings.OPEN_AI_KEY

DEFAULT_ANSWER_PROMPT = """
You are a human with a diverse taste in food. 
Generate a response with your top 3 favorite foods. 
Be diverse, creative, and realistic in your choices. 
Be conversational, engaging, and helpful.
Include whether these choices make you vegetarian, vegan, or neither. 

Format your response as JSON with fields:
- foods (array of 3 unique strings)
- is_vegetarian (boolean)
- is_vegan (boolean)
- response (string)
"""

CHATBOT_PROMPT = """
You are a friendly food enthusiast chatbot named FoodieBot.
Your purpose is to discuss food preferences, recipes, and culinary topics.
Be conversational, engaging, and helpful.
If the user shares their favorite foods, acknowledge them and ask follow-up questions.
Keep your responses brief and friendly.
"""

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=str(OPEN_AI_KEY))

    def ask_favorite_foods(self):
        """Simulates ChatGPT A asking about favorite foods"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are food enthusiast. Your task is to ask the user about their three favorite foods."},
                {"role": "user", "content": "Generate a question asking about someone's top 3 favorite foods."}
            ]
        )
        question = response.choices[0].message.content

        return question

    def generate_food_preferences(self, question):
        """Simulates ChatGPT B responding with favorite foods and stores conversation history"""
        conversation = Conversation.objects.create()  # Create conversation instance

        # Store the initial question as the first message
        Message.objects.create(
            conversation=conversation,
            content=question,
            role='ChatgptA'  
        )


        #Chatgpt B responds here
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=1.2,
            top_p=0.9,
            messages=[
                {"role": "system", "content": DEFAULT_ANSWER_PROMPT},
                {"role": "user", "content": question}
            ]
        )

        content = response.choices[0].message.content


        try:
            # Parse and store JSON response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end] if start >= 0 and end > start else '{}'
            
            data = json.loads(json_str)
            foods = data.get("foods", [])
            reply = data.get("response", "")
            is_vegetarian = data.get("is_vegetarian", False)
            is_vegan = data.get("is_vegan", False)
            
            # Extract response message and store it
            Message.objects.create(
                conversation=conversation,
                content=reply,
                role='ChatgptB'
            )

            # Update conversation diet flags
            conversation.is_vegetarian = is_vegetarian
            conversation.is_vegan = is_vegan
            conversation.save()

            # Save food preferences
            for i, food in enumerate(foods):
                FoodPreference.objects.create(
                    conversation=conversation,
                    food_name=food,
                    rank=i + 1
                )

            return {
                "foods": foods,
                "is_vegetarian": is_vegetarian,
                "is_vegan": is_vegan,
                "conversation_id": conversation.id
            }

        # except json.JSONDecodeError:
        except Exception as e:
            # Fallback to random preferences if JSON parsing fails
            return self._generate_random_preferences(conversation)

    def _generate_random_preferences(self, conversation):
        """Fallback method if JSON extraction fails"""
        vegetarian_foods = ["pizza", "pasta", "salad", "avocado toast", "veggie burger", "risotto"]
        vegan_foods = ["tofu stir-fry", "chickpea curry", "mushroom risotto", "vegan pizza", "lentil soup"]
        non_veg_foods = ["steak", "sushi", "chicken curry", "lamb chops", "seafood pasta"]

        is_vegan = random.random() < 0.2
        is_vegetarian = is_vegan or random.random() < 0.3

        if is_vegan:
            foods = random.sample(vegan_foods, 3)
        elif is_vegetarian:
            foods = random.sample(vegetarian_foods + vegan_foods, 3)
        else:
            foods = random.sample(vegetarian_foods + non_veg_foods, 3)

        # Store fallback preferences
        conversation.is_vegetarian = is_vegetarian
        conversation.is_vegan = is_vegan
        conversation.save()

        for i, food in enumerate(foods):
            FoodPreference.objects.create(
                conversation=conversation,
                food_name=food,
                rank=i + 1
            )

        return {
            "foods": foods,
            "is_vegetarian": is_vegetarian,
            "is_vegan": is_vegan
        }
        
    def create_user_conversation(self):
        """Creates a new conversation for a real user"""
        conversation = Conversation.objects.create(is_user_conversation=True)
        
        # Generate initial chatbot message
        initial_message = "Hi there! I'm FoodieBot. I love talking about food! What are your top 3 favorite foods?"
        
        Message.objects.create(
            conversation=conversation,
            content=initial_message,
            role='ChatBot'
        )
        
        return {
            "conversation_id": conversation.id,
            "message": initial_message
        }
    
    def chat_with_user(self, conversation_id, user_message):
        """Process a user message and generate a chatbot response"""
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            
            # Store user message
            Message.objects.create(
                conversation=conversation,
                content=user_message,
                role='User'
            )
            
            # Get conversation history (last 10 messages for context)
            messages = Message.objects.filter(conversation=conversation).order_by('created_at')[:10]
            conversation_history = []
            
            for msg in messages:
                role = "assistant" if msg.role == "ChatBot" else "user"
                conversation_history.append({"role": role, "content": msg.content})
            
            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": CHATBOT_PROMPT},
                    *conversation_history
                ]
            )
            
            bot_response = response.choices[0].message.content
            
            # Store bot response
            Message.objects.create(
                conversation=conversation,
                content=bot_response,
                role='ChatBot'
            )
            
            # Check for food preferences in user message
            self._extract_food_preferences(conversation, user_message)
            
            return {
                "message": bot_response
            }
        
        except Conversation.DoesNotExist:
            return {
                "error": "Conversation not found"
            }
    
    def _extract_food_preferences(self, conversation, user_message):
        """Attempt to extract food preferences from user messages"""
        # Ask GPT to extract food preferences if they exist
        extraction_prompt = f"""
        Extract food preferences from this message if they exist:
        "{user_message}"
        
        If the user mentions foods they like, return them as a JSON object with:
        - foods: array of food names mentioned (up to 3)
        - is_vegetarian: boolean (true if all foods appear vegetarian)
        - is_vegan: boolean (true if all foods appear vegan)
        
        If no food preferences are mentioned, return an empty JSON object {{}}.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You extract food preferences from text."},
                    {"role": "user", "content": extraction_prompt}
                ]
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                foods = data.get("foods", [])
                if foods:
                    is_vegetarian = data.get("is_vegetarian", False)
                    is_vegan = data.get("is_vegan", False)
                    
                    # Update conversation flags
                    conversation.is_vegetarian = is_vegetarian
                    conversation.is_vegan = is_vegan
                    conversation.save()
                    
                    # Save extracted food preferences
                    #TODO can add bulk creation
                    existing_foods = FoodPreference.objects.filter(conversation=conversation)
                    if not existing_foods.exists():
                        for i, food in enumerate(foods[:3]):
                            FoodPreference.objects.create(
                                conversation=conversation,
                                food_name=food,
                                rank=i + 1
                            )
        except:
            # Silently fail - we don't want to disrupt the chat if preference extraction fails, but we do want to log it later
            pass