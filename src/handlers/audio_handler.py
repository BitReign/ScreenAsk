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
from src.core.config import Config

class AudioHandler:
    def __init__(self):
        self.config = Config()
        self.recording = False
        self.audio_data = None
        self.recording_stream = None
        
        # Initialize speech recognition if available
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            # Don't use sr.Microphone() as it depends on PyAudio
            # We'll use sounddevice for recording and sr.AudioFile for transcription
            self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        
        # Initialize OpenAI handler for Whisper (lazy initialization)
        self.openai_handler = None
        
        # Audio recording settings
        self.channels = 1
        self.rate = 44100
        
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
        """Start continuous recording audio using sounddevice"""
        if not AUDIO_AVAILABLE:
            print("Audio libraries not available - cannot record audio")
            return False
            
        try:
            if self.recording:
                print("Already recording, ignoring start request")
                return False
                
            self.recording = True
            self.audio_data = []
            
            print("Starting continuous recording...")
            
            # Start recording stream
            self.recording_stream = sd.InputStream(
                samplerate=self.rate,
                channels=self.channels,
                dtype='int16',
                callback=self._recording_callback
            )
            self.recording_stream.start()
            
            return True
        except Exception as e:
            print(f"Error during recording: {e}")
            self.recording = False
            return False
    
    def _recording_callback(self, indata, frames, time, status):
        """Callback for continuous recording"""
        if status:
            print(f"Recording status: {status}")
        
        if self.recording and self.audio_data is not None:
            self.audio_data.append(indata.copy())
    
    def stop_recording(self):
        """Stop continuous recording audio"""
        if not self.recording:
            print("Not currently recording, ignoring stop request")
            return
            
        try:
            self.recording = False
            
            # Stop the recording stream
            if hasattr(self, 'recording_stream') and self.recording_stream:
                self.recording_stream.stop()
                self.recording_stream.close()
                self.recording_stream = None
            
            # Convert collected audio data to numpy array
            if self.audio_data and len(self.audio_data) > 0:
                self.audio_data = np.concatenate(self.audio_data, axis=0)
                print(f"Recording stopped. Captured {len(self.audio_data)} samples.")
            else:
                print("Recording stopped. No audio data captured.")
                self.audio_data = None
                
        except Exception as e:
            print(f"Error stopping recording: {e}")
            self.recording = False
    
    def save_recording(self, filename="temp_recording.wav"):
        """Save recorded audio to file"""
        if not AUDIO_AVAILABLE or self.audio_data is None:
            print("Audio data not available - cannot save recording")
            return None
            
        try:
            # Check if we have valid audio data
            if len(self.audio_data) == 0:
                print("No audio data to save")
                return None
                
            # Save using soundfile
            sf.write(filename, self.audio_data, self.rate)
            print(f"Audio saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving recording: {e}")
            return None
    
    def transcribe_audio(self, filename="temp_recording.wav"):
        """Transcribe audio file to text"""
        # Reload config to get latest settings
        self.config.load_config()
        transcription_service = self.config.get('Audio', 'transcription_service', 'google')
        
        if transcription_service == 'openai_whisper':
            return self.transcribe_with_whisper(filename)
        else:
            return self.transcribe_with_google(filename)
    
    def transcribe_with_google(self, filename="temp_recording.wav"):
        """Transcribe audio file using Google Speech Recognition"""
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
    
    def transcribe_with_whisper(self, filename="temp_recording.wav"):
        """Transcribe audio file using OpenAI Whisper"""
        # Initialize OpenAI handler if not already done
        if self.openai_handler is None:
            try:
                from openai_handler import OpenAIHandler
                self.openai_handler = OpenAIHandler()
            except ImportError as e:
                print(f"Error importing OpenAI handler: {e}")
                return None
        
        if not self.openai_handler.is_configured():
            print("OpenAI API not configured - cannot use Whisper")
            return None
            
        try:
            with open(filename, 'rb') as audio_file:
                # Convert language code for Whisper (uses 2-letter codes)
                language_full = self.config.get('Audio', 'language', 'en-US')
                language_code = language_full[:2].lower()
                
                # Ensure Turkish is properly handled
                if language_full == 'tr-TR':
                    language_code = 'tr'
                
                transcript = self.openai_handler.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language_code
                )
                return transcript.text
        except Exception as e:
            print(f"Error transcribing audio with Whisper: {e}")
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