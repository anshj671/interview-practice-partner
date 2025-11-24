
import threading
from typing import Optional, Callable
import time

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    pyttsx3 = None

class VoiceInterface:
    
    
    def __init__(self, language: str = "en-US", rate: int = 150):
        self.language = language
        self.rate = rate
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        self.is_listening = False
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', rate)
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
            except Exception as e:
                print(f"Warning: Could not initialize TTS engine: {e}")
                self.tts_engine = None
        else:
            self.tts_engine = None
            print("Warning: pyttsx3 not available. Voice output disabled.")
        
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
            except Exception as e:
                print(f"Warning: Could not initialize microphone: {e}")
                self.microphone = None
        else:
            self.microphone = None
            self.recognizer = None
            print("Warning: speech_recognition not available. Voice input disabled.")
    
    def speak(self, text: str, async_mode: bool = False):
        
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
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")
            print(f"[Agent]: {text}")
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 30) -> Optional[str]:
        
        if not SPEECH_RECOGNITION_AVAILABLE or not self.microphone or not self.recognizer:
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
        
        self.is_listening = False

