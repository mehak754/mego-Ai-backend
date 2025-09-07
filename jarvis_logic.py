import os
import glob
import webbrowser
import datetime
import subprocess
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    gemini_available = True
    print("Gemini AI initialized successfully")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    gemini_available = False


def say(text):
    """Print the AI response (no voice)"""
    print("Mego:", text)


def take_command():
    """Get text input instead of voice"""
    return input("You: ").strip().lower()


def get_current_time():
    """Return current time in a readable format"""
    return datetime.datetime.now().strftime("%I:%M %p")


def open_application(app_name):
    """Fake app opening for headless server"""
    return f"(Simulated) Opening {app_name}"


def play_music(query):
    """Simulated music playback"""
    return "(Simulated) Playing music..."


def ask_gemini(query):
    """Ask Gemini AI for response"""
    if not gemini_available:
        return "I'm sorry, the AI service is currently unavailable."

    try:
        prompt = f"""You are Mego, a friendly AI assistant. Respond to the following query in a helpful, conversational manner. 
        Keep your response concise and natural for voice output (under 100 words).

        Query: {query}

        Response:"""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return "I'm having trouble connecting to the AI service right now."


def handle_query(query):
    if not query or "sorry" in query:
        return ""

    # Website opening
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
        ["chatgpt", "https://chat.openai.com"],
        ["spotify", "https://www.spotify.com"],
        ["instagram", "https://www.instagram.com"],
        ["x", "https://www.x.com"],
        ["snapchat", "https://www.snapchat.com"]
    ]

    for site in sites:
        if f"open {site[0]}" in query:
            webbrowser.open(site[1])
            return f"Opening {site[0]}"

    if "play music" in query or "play song" in query:
        return play_music(query)

    if "time" in query:
        return f"The current time is {get_current_time()}"

    for app in ["facetime", "music", "calculator", "calendar"]:
        if f"open {app}" in query:
            return open_application(app)

    intelligence_phrases = [
        "use your intelligence",
        "what do you think",
        "can you help me with",
        "how can i",
        "what is",
        "who is",
        "why is",
        "where is",
        "when should i",
        "should i"
    ]

    if any(phrase in query for phrase in intelligence_phrases):
        return ask_gemini(query)

    if any(word in query for word in ["exit", "quit", "stop", "good bye"]):
        return "Goodbye! Have a great day!"

    return ask_gemini(query)

