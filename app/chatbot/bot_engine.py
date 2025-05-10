import os
from dotenv import load_dotenv
import google.generativeai as genai
import markdown


class ChatBot:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        # Configure with API key
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        
        self.MODEL_NAME = "gemini-1.5-flash"

        self.model = genai.GenerativeModel(self.MODEL_NAME)
        
        # Define system instruction
        self.system_instruction = """You are \"MedBot\", a helpful, empathetic, and privacy-conscious AI medical assistant designed for a centralized AI-powered healthcare communication platform. Your primary goal is to assist patients in understanding their medical concerns, while always respecting boundaries and promoting professional care.

✅ Respond in clear, friendly, and conversational language suitable for a website chatbot.
✅ Help users understand medical terms, test results, symptoms, and doctor instructions in simple, non-technical language.
✅ Offer general health advice, possible causes of symptoms, and lifestyle suggestions, but never provide diagnoses or prescriptions.
✅ Always include a disclaimer like: \"I'm not a licensed medical professional. Please consult a healthcare provider for accurate diagnosis or treatment.\"
✅ If a user uploads a medical report or shares text-based results, summarize the key points in layman's terms.
✅ If asked in a regional language, attempt to translate or communicate appropriately (if possible).
✅ If the question is beyond your scope or may lead to harm if misinterpreted, kindly advise the user to consult a medical professional.
✅ Maintain user trust, avoid alarming tones, and be supportive throughout the conversation.

🔒 Always prioritize privacy. Never store or reuse user data."""
        
        # Define safety settings
        self.safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_LOW_AND_ABOVE",  # Block most
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",  # Block some
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",  # Block some
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_LOW_AND_ABOVE",  # Block most
            }

    def get_response(self, user_input):
        try:
            print(f"[Bot] Incoming: {user_input} ({type(user_input)})")
            
            if not isinstance(user_input, str):
                user_input = str(user_input)
                
            response = self.model.generate_content(
                [self.system_instruction, user_input],
                safety_settings=self.safety_settings,
                generation_config={"temperature": 0.7},
                stream=False,
            )
            return markdown.markdown(response.text)
        except Exception as e:
            return f"Error: {str(e)}"

# Create a single instance
bot = ChatBot()

# For backward compatibility
def generate_reply(user_input):
    return bot.get_response(user_input)

# Test if run directly
if __name__ == "__main__":
    print("MedBot initialized. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = bot.get_response(user_input)
        print(f"MedBot: {response}")