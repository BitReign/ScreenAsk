import pyaudio
import wave
import speech_recognition as sr
import threading
import time
import os
from config import Config

class AudioHandler:
    def __init__(self):
        self.config = Config()
        self.recording = False
        self.frames = []
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio recording settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.record_duration = int(self.config.get('Audio', 'record_duration', '5'))
        
        # Calibrate microphone for ambient noise
        self.calibrate_microphone()
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                print("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)
                print("Microphone calibrated.")
        except Exception as e:
            print(f"Error calibrating microphone: {e}")
    
    def start_recording(self):
        """Start recording audio"""
        try:
            self.recording = True
            self.frames = []
            
            audio = pyaudio.PyAudio()
            stream = audio.open(format=self.format,
                              channels=self.channels,
                              rate=self.rate,
                              input=True,
                              frames_per_buffer=self.chunk)
            
            print(f"Recording for {self.record_duration} seconds...")
            
            for i in range(0, int(self.rate / self.chunk * self.record_duration)):
                if not self.recording:
                    break
                data = stream.read(self.chunk)
                self.frames.append(data)
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
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
        try:
            audio = pyaudio.PyAudio()
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            audio.terminate()
            return filename
        except Exception as e:
            print(f"Error saving recording: {e}")
            return None
    
    def transcribe_audio(self, filename="temp_recording.wav"):
        """Transcribe audio file to text"""
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
        """Listen for speech using microphone directly"""
        try:
            with self.microphone as source:
                print("Listening for speech...")
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language=self.config.get('Audio', 'language', 'en-US'))
                return text
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error listening for speech: {e}")
            return None 