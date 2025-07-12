try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    AUDIO_AVAILABLE = True
    print("✓ Audio recording available via sounddevice")
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: Audio libraries not available - voice input disabled")

import wave
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: SpeechRecognition not available - voice input disabled")

import threading
import time
import os
from config import Config

class AudioHandler:
    def __init__(self):
        self.config = Config()
        self.recording = False
        self.audio_data = None
        
        # Initialize speech recognition if available
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            # Don't use sr.Microphone() as it depends on PyAudio
            # We'll use sounddevice for recording and sr.AudioFile for transcription
            self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        
        # Audio recording settings
        self.channels = 1
        self.rate = 44100
        self.record_duration = int(self.config.get('Audio', 'record_duration', '5'))
        
        # Set default input device if available
        if AUDIO_AVAILABLE:
            try:
                # Get default input device
                device_info = sd.query_devices(kind='input')
                print(f"Using audio device: {device_info['name']}")
            except Exception as e:
                print(f"Warning: Could not query audio devices: {e}")
        
        # Calibrate microphone for ambient noise
        self.calibrate_microphone()
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if not SPEECH_RECOGNITION_AVAILABLE or not AUDIO_AVAILABLE:
            print("Audio recording not available - skipping microphone calibration")
            return
            
        # Skip microphone calibration since we're using sounddevice instead of PyAudio
        print("Skipping microphone calibration (not needed with sounddevice)")
    
    def start_recording(self):
        """Start recording audio using sounddevice"""
        if not AUDIO_AVAILABLE:
            print("Audio libraries not available - cannot record audio")
            return False
            
        try:
            self.recording = True
            print(f"Recording for {self.record_duration} seconds...")
            
            # Record audio using sounddevice
            self.audio_data = sd.rec(
                int(self.record_duration * self.rate),
                samplerate=self.rate,
                channels=self.channels,
                dtype='int16'
            )
            
            # Wait for recording to complete
            sd.wait()
            
            print("Recording finished.")
            return True
        except Exception as e:
            print(f"Error during recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop recording audio"""
        self.recording = False
    
    def save_recording(self, filename="temp_recording.wav"):
        """Save recorded audio to file"""
        if not AUDIO_AVAILABLE or self.audio_data is None:
            print("Audio data not available - cannot save recording")
            return None
            
        try:
            # Save using soundfile
            sf.write(filename, self.audio_data, self.rate)
            return filename
        except Exception as e:
            print(f"Error saving recording: {e}")
            return None
    
    def transcribe_audio(self, filename="temp_recording.wav"):
        """Transcribe audio file to text"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            print("Speech recognition not available - cannot transcribe audio")
            return None
            
        try:
            with sr.AudioFile(filename) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=self.config.get('Audio', 'language', 'en-US'))
                return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def record_and_transcribe(self):
        """Record audio and transcribe to text"""
        if self.start_recording():
            filename = self.save_recording()
            if filename:
                text = self.transcribe_audio(filename)
                # Clean up temporary file
                try:
                    os.remove(filename)
                except:
                    pass
                return text
        return None
    
    def listen_for_speech(self, timeout=5):
        """Listen for speech using sounddevice recording"""
        if not SPEECH_RECOGNITION_AVAILABLE or not AUDIO_AVAILABLE:
            print("Audio recording not available - cannot listen for speech")
            return None
            
        try:
            print("Listening for speech...")
            
            # Record audio using sounddevice for the specified timeout
            audio_data = sd.rec(
                int(timeout * self.rate),
                samplerate=self.rate,
                channels=self.channels,
                dtype='int16'
            )
            
            # Wait for recording to complete
            sd.wait()
            
            # Save to temporary file
            temp_filename = "temp_listen_recording.wav"
            sf.write(temp_filename, audio_data, self.rate)
            
            # Transcribe the audio
            text = self.transcribe_audio(temp_filename)
            
            # Clean up temporary file
            try:
                os.remove(temp_filename)
            except:
                pass
                
            return text
        except Exception as e:
            print(f"Error listening for speech: {e}")
            return None 