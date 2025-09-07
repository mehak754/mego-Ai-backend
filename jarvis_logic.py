import os
import glob
import pyttsx3
import webbrowser
import datetime
import subprocess
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Use correct key name here!
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

# Initialize Gemini model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    gemini_available = True
    print("Gemini AI initialized successfully")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    gemini_available = False


def say(text):
    """Convert text to speech"""
    print("Mego:", text)
    engine.say(text)
    engine.runAndWait()


def get_current_time():
    """Return current time in a readable format"""
    return datetime.datetime.now().strftime("%I:%M %p")


def open_application(app_name):
    """Open applications based on command"""
    app_paths = {
        "facetime": "/System/Applications/FaceTime.app",
        "music": "/System/Applications/Music.app",
        "calculator": "/System/Applications/Calculator.app",
        "calendar": "/System/Applications/Calendar.app"
    }

    if app_name in app_paths:
        os.system(f"open {app_paths[app_name]}")
        return f"Opening {app_name}"
    else:
        return f"Sorry, I don't know how to open {app_name}"


def play_music(query):
    """Play music from the specified folder"""
    music_folder = "/Users/tlc/Downloads"
    songs = []

    # Recursive search for all audio files
    audio_extensions = ('*.mp3', '*.m4a', '*.wav', '*.flac')
    for extension in audio_extensions:
        for filepath in glob.glob(os.path.join(music_folder, "**/" + extension), recursive=True):
            song_name = os.path.basename(filepath).rsplit('.', 1)[0]
            songs.append([song_name, filepath])

    if not songs:
        return "No songs found in your music folder."

    # If a specific song is requested
    for song in songs:
        if song[0].lower() in query:
            os.system(f"open -a Music \"{song[1]}\"")
            return f"Playing {song[0]}"

    # Play a random song if no specific song requested
    random_song = random.choice(songs)
    os.system(f"open -a Music \"{random_song[1]}\"")
    return f"Playing music: {random_song[0]}"


def ask_gemini(query):
    """Query Gemini AI for responses"""
    if not gemini_available:
        return "I'm sorry, the AI service is currently unavailable."

    try:
        prompt = f"""You are Mego, a friendly AI assistant. Respond to the following query in a helpful, conversational manner. 
        Keep your response concise and natural for voice output (under 100 words).

        Query: {query}

        Response:"""

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return "I'm having trouble connecting to the AI service right now."


def handle_query(query):
    """Process the user query and return appropriate response"""
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

    # Music playing
    if "play music" in query or "play song" in query:
        return play_music(query)

    # Time query
    if "time" in query:
        return f"The current time is {get_current_time()}"

    # Application opening
    for app in ["facetime", "music", "calculator", "calendar"]:
        if f"open {app}" in query:
            return open_application(app)

    # AI intelligence queries
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

    # Exit command
    if any(word in query for word in ["exit", "quit", "stop", "good bye"]):
        return "Goodbye! Have a great day!"

    # Default response for unrecognized queries
    return ask_gemini(query)


if __name__ == '__main__':
    say("Hello! I am Mego A.I. How can I help you today?")

    while True:
        # ⌨️ User types command instead of speaking
        query = input("You: ").lower()

        if query:
            response = handle_query(query)
            if response:
                say(response)

                # Check if it's an exit command
                if any(word in response for word in ["Goodbye", "exit", "quit"]):
                    break

           
