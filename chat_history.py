import json
import time
from typing import Dict, List, Optional
from datetime import datetime

class ChatHistory:
    """Handle chat history between user and AI"""
    
    def __init__(self):
        self.chat_history = []
        self.max_history = 50  # Keep last 50 messages
        
    def add_message(self, sender: str, message: str, timestamp: float = None, metadata: dict = None):
        """Add a message to chat history
        
        Args:
            sender: 'user' or 'ai'
            message: The message content
            timestamp: Optional timestamp, defaults to current time
            metadata: Optional metadata dict (e.g., coordinates, processing time)
        """
        if timestamp is None:
            timestamp = time.time()
        
        chat_message = {
            'sender': sender,
            'message': message,
            'timestamp': timestamp,
            'datetime': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'metadata': metadata or {}
        }
        
        self.chat_history.append(chat_message)
        
        # Keep only the last max_history messages
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]
        
        print(f"Chat history: Added {sender} message: {message[:50]}...")
        
    def get_recent_messages(self, count: int = 10) -> List[Dict]:
        """Get the most recent messages"""
        return self.chat_history[-count:] if self.chat_history else []
    
    def get_all_messages(self) -> List[Dict]:
        """Get all messages"""
        return self.chat_history.copy()
    
    def clear_history(self):
        """Clear all chat history"""
        self.chat_history.clear()
        print("Chat history cleared")
    
    def get_message_count(self) -> int:
        """Get total number of messages"""
        return len(self.chat_history)
    
    def save_to_file(self, filename: str = "chat_history.json"):
        """Save chat history to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
            print(f"Chat history saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
    
    def load_from_file(self, filename: str = "chat_history.json"):
        """Load chat history from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
            print(f"Chat history loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"Chat history file {filename} not found")
            return False
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return False
    
    def get_last_user_message(self) -> Optional[Dict]:
        """Get the last user message"""
        for message in reversed(self.chat_history):
            if message['sender'] == 'user':
                return message
        return None
    
    def get_last_ai_message(self) -> Optional[Dict]:
        """Get the last AI message"""
        for message in reversed(self.chat_history):
            if message['sender'] == 'ai':
                return message
        return None
    
    def export_conversation(self, format: str = 'text') -> str:
        """Export conversation in specified format
        
        Args:
            format: 'text' or 'json'
        """
        if format == 'json':
            return json.dumps(self.chat_history, indent=2, ensure_ascii=False)
        
        # Text format
        lines = []
        for message in self.chat_history:
            timestamp = message['datetime']
            sender = message['sender'].upper()
            content = message['message']
            lines.append(f"[{timestamp}] {sender}: {content}")
        
        return '\n'.join(lines) 