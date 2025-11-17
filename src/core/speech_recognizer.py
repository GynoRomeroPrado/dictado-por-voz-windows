"""
Speech recognition module
Handles microphone input and speech-to-text conversion
"""

import speech_recognition as sr
import threading
import queue
from typing import Callable, Optional

# Handle both relative and absolute imports
try:
    from ..utils.config import config
except ImportError:
    from utils.config import config


class SpeechRecognizer:
    """Manages speech recognition using various engines"""

    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize the speech recognizer

        Args:
            callback: Function to call with recognized text
        """
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.callback = callback
        self.is_listening = False
        self.recognition_thread = None
        self.text_queue = queue.Queue()

        # Load configuration
        self.language = config.get('language', 'es-ES')
        self.engine = config.get('recognition.engine', 'windows')
        self.confidence_threshold = config.get('recognition.confidence_threshold', 0.7)

        # Configure recognizer
        self._configure_recognizer()

    def _configure_recognizer(self):
        """Configure the recognizer with settings from config"""
        try:
            # Energy threshold for ambient noise
            energy_threshold = config.get('recognition.energy_threshold', 4000)
            self.recognizer.energy_threshold = energy_threshold

            # Dynamic energy adjustment
            dynamic_energy = config.get('recognition.dynamic_energy', True)
            self.recognizer.dynamic_energy_threshold = dynamic_energy

            # Pause threshold (how much silence before phrase is complete)
            pause_threshold = config.get('recognition.pause_threshold', 0.8)
            self.recognizer.pause_threshold = pause_threshold

            # Non-speaking duration
            non_speaking = config.get('recognition.non_speaking_duration', 0.5)
            self.recognizer.non_speaking_duration = non_speaking

        except Exception as e:
            print(f"Error configuring recognizer: {e}")

    def _get_microphone(self):
        """Get or initialize microphone"""
        if self.microphone is None:
            try:
                self.microphone = sr.Microphone()
                # Adjust for ambient noise
                with self.microphone as source:
                    print("Adjusting for ambient noise... Please wait.")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Ready for speech recognition.")
            except Exception as e:
                print(f"Error initializing microphone: {e}")
                return None
        return self.microphone

    def recognize_once(self) -> Optional[str]:
        """
        Listen for speech once and return recognized text

        Returns:
            str: Recognized text or None if recognition failed
        """
        mic = self._get_microphone()
        if mic is None:
            return None

        try:
            with mic as source:
                print("Listening...")
                audio = self.recognizer.listen(source)

            print("Recognizing...")
            text = self._recognize_audio(audio)
            return text

        except sr.WaitTimeoutError:
            print("Listening timeout")
            return None
        except Exception as e:
            print(f"Error in recognize_once: {e}")
            return None

    def _recognize_audio(self, audio) -> Optional[str]:
        """
        Recognize audio using configured engine

        Args:
            audio: Audio data to recognize

        Returns:
            str: Recognized text or None
        """
        try:
            # Try different recognition engines based on config
            if self.engine == 'google':
                text = self.recognizer.recognize_google(audio, language=self.language)
            elif self.engine == 'sphinx':
                text = self.recognizer.recognize_sphinx(audio, language=self.language)
            else:  # Default to Windows (recognize_whisper requires additional setup)
                # Windows Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio, language=self.language)
                except sr.RequestError:
                    # Fallback to Google if Windows SR is not available
                    print("Windows SR not available, using Google")
                    text = self.recognizer.recognize_google(audio, language=self.language)

            if text:
                print(f"Recognized: {text}")
                return text
            else:
                return None

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"Error recognizing audio: {e}")
            return None

    def start_listening(self):
        """Start continuous listening in background thread"""
        if self.is_listening:
            print("Already listening")
            return

        self.is_listening = True
        self.recognition_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.recognition_thread.start()
        print("Started continuous listening")

    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self.recognition_thread:
            self.recognition_thread.join(timeout=2)
        print("Stopped listening")

    def _listen_loop(self):
        """Background listening loop"""
        mic = self._get_microphone()
        if mic is None:
            self.is_listening = False
            return

        with mic as source:
            while self.is_listening:
                try:
                    print("Listening (continuous)...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)

                    # Recognize in separate thread to avoid blocking
                    threading.Thread(
                        target=self._process_audio,
                        args=(audio,),
                        daemon=True
                    ).start()

                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Error in listen loop: {e}")
                    if not self.is_listening:
                        break

    def _process_audio(self, audio):
        """Process audio in background thread"""
        try:
            text = self._recognize_audio(audio)
            if text and self.callback:
                self.callback(text)
            elif text:
                self.text_queue.put(text)
        except Exception as e:
            print(f"Error processing audio: {e}")

    def get_text(self) -> Optional[str]:
        """
        Get recognized text from queue (non-blocking)

        Returns:
            str: Recognized text or None if queue is empty
        """
        try:
            return self.text_queue.get_nowait()
        except queue.Empty:
            return None

    def set_language(self, language: str):
        """
        Change recognition language

        Args:
            language: Language code (e.g., 'es-ES', 'en-US')
        """
        self.language = language
        config.set('language', language)
        print(f"Language changed to: {language}")

    def set_callback(self, callback: Callable):
        """
        Set callback function for recognized text

        Args:
            callback: Function to call with recognized text
        """
        self.callback = callback

    def get_available_languages(self):
        """
        Get list of available languages

        Returns:
            list: List of language codes
        """
        return config.get('alternative_languages', [
            'es-ES', 'en-US', 'es-MX', 'fr-FR', 'de-DE', 'it-IT', 'pt-BR'
        ])

    def test_microphone(self) -> bool:
        """
        Test if microphone is working

        Returns:
            bool: True if microphone is working
        """
        try:
            mic = self._get_microphone()
            if mic is None:
                return False

            with mic as source:
                print("Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=3)
                text = self._recognize_audio(audio)
                return text is not None

        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False
