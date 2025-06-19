import os
import random
import webbrowser
import time
import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import soundfile as sf
import requests

# Initialize the speech engine for text-to-speech
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Captures voice input using sounddevice and recognizes it using Google API."""
    recognizer = sr.Recognizer()
    print("Listening...")
    speak("I am listening...")
    
    duration = 5  # Duration to listen in seconds
    sample_rate = 16000  # Sampling rate for the recording
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to finish

    # Save the recording to a temporary file
    temp_file = "temp.wav"
    sf.write(temp_file, audio_data, sample_rate)

    # Recognize speech from the saved audio file
    with sr.AudioFile(temp_file) as source:
        audio = recognizer.record(source)
        try:
            # Using Google's speech recognition API to transcribe the audio
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, the speech recognition service is down.")
            return ""

def open_website(command):
    """Opens a website based on the command."""
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com"
    }
    
    for key in websites:
        if key in command:
            webbrowser.open(websites[key])
            return True
    return False

def tell_joke():
    """Tells a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "I told my computer I needed a break, and now it won’t stop sending me KitKat ads!"
    ]
    joke = random.choice(jokes)
    speak(joke)

def play_music(song_name):
    """Plays a specific song based on the command."""
    songs = {
        "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
        "blinding lights": "https://www.youtube.com/watch?v=4NRXx6U8ABQ"
    }

    song_url = songs.get(song_name.lower(), None)
    
    if song_url:
        speak(f"Playing {song_name}.")
        webbrowser.open(song_url)
    else:
        speak(f"Sorry, I couldn't find the song {song_name}.")

def pause_music():
    """Pauses the music by opening the current song URL in a new tab."""
    speak("Pausing the music.")
    # In a real-world scenario, you would control the web player here, but we're simulating it by opening the link.
    webbrowser.open("https://www.youtube.com")

def get_weather():
    """Fetches current weather information."""
    # You should replace 'your_api_key_here' with your actual OpenWeatherMap API key
    api_key = "92a4f0d600be36f399cba481a2a13343"
    city = "bangalore"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            main = data['main']
            weather_description = data['weather'][0]['description']
            temperature = main['temp'] - 273.15  # Convert temperature from Kelvin to Celsius
            speak(f"The temperature is {temperature:.2f}°C with {weather_description}.")
        else:
            speak("Sorry, I couldn't fetch the weather information.")
    except Exception as e:
        speak(f"Sorry, there was an error fetching the weather. Error: {str(e)}")

def main():
    """Main function that runs the assistant."""
    speak("Hello, I am your assistant.")
    
    while True:
        command = listen_command()

        if 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
        elif 'open' in command:
            if not open_website(command):
                speak("I couldn't find the website.")
        elif 'time' in command:
            current_time = time.strftime("%I:%M %p")
            speak(f"The time is {current_time}.")
        elif 'joke' in command:
            tell_joke()
        elif 'play music' in command:
            song_name = command.replace("play music", "").strip()
            play_music(song_name)
        elif 'pause' in command:
            pause_music()
        elif 'weather' in command:
            get_weather()
        else:
            speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()
