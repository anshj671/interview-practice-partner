"""
Voice interface for the Interview Practice Partner
Supports both voice input (speech recognition) and voice output (text-to-speech)
"""
import speech_recognition as sr
import pyttsx3
import threading
from typing import Optional, Callable
import time

class VoiceInterface:
    """Handles voice input and output for the interview agent"""
    
    def __init__(self, language: str = "en-US", rate: int = 150):
        self.language = language
        self.rate = rate
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        self.is_listening = False
        
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', rate)
            # Try to set a pleasant voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            print(f"Warning: Could not initialize TTS engine: {e}")
            self.tts_engine = None
        
        # Initialize microphone
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Warning: Could not initialize microphone: {e}")
            self.microphone = None
    
    def speak(self, text: str, async_mode: bool = False):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            async_mode: If True, speak in background thread
        """
        if not self.tts_engine:
            print(f"[Agent]: {text}")
            return
        
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str):
        """Synchronous speech output"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")
            print(f"[Agent]: {text}")
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 30) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for a phrase
        
        Returns:
            Recognized text or None if error/timeout
        """
        if not self.microphone:
            print("Microphone not available. Please use text input.")
            return None
        
        try:
            with self.microphone as source:
                print("[Listening...]")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("[Processing...]")
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"[You]: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that. Could you repeat?")
                return None
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
                return None
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None
    
    def listen_continuous(
        self, 
        callback: Callable[[str], None],
        stop_phrase: str = "stop listening"
    ):
        """
        Continuously listen and call callback with recognized text
        
        Args:
            callback: Function to call with recognized text
            stop_phrase: Phrase to stop listening
        """
        self.is_listening = True
        print(f"Continuous listening started. Say '{stop_phrase}' to stop.")
        
        while self.is_listening:
            text = self.listen(timeout=1)
            if text:
                if stop_phrase.lower() in text.lower():
                    self.is_listening = False
                    break
                callback(text)
            time.sleep(0.1)
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False

