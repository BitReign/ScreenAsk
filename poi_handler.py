import json
import time
from typing import Dict, List, Optional, Tuple

class POIHandler:
    """Handle Point of Interest data from structured AI responses"""
    
    def __init__(self):
        self.current_poi = None
        self.poi_history = []
        self.max_history = 10  # Keep last 10 POIs
        
    def set_current_poi(self, x: int, y: int, radius: int, text: str):
        """Set the current point of interest"""
        poi_data = {
            'x': x,
            'y': y,
            'radius': radius,
            'text': text,
            'timestamp': time.time()
        }
        
        # Add to history
        self.poi_history.append(poi_data)
        
        # Keep only the last max_history items
        if len(self.poi_history) > self.max_history:
            self.poi_history = self.poi_history[-self.max_history:]
        
        # Set as current
        self.current_poi = poi_data
        
        print(f"POI set: ({x}, {y}) with radius {radius}")
        
    def get_current_poi(self) -> Optional[Dict]:
        """Get the current point of interest"""
        return self.current_poi
    
    def get_poi_coordinates(self) -> Optional[Tuple[int, int]]:
        """Get just the coordinates of current POI"""
        if self.current_poi:
            return (self.current_poi['x'], self.current_poi['y'])
        return None
    
    def get_poi_radius(self) -> Optional[int]:
        """Get the radius of current POI"""
        if self.current_poi:
            return self.current_poi['radius']
        return None
    
    def get_poi_text(self) -> Optional[str]:
        """Get the text of current POI"""
        if self.current_poi:
            return self.current_poi['text']
        return None
    
    def get_poi_history(self) -> List[Dict]:
        """Get the POI history"""
        return self.poi_history.copy()
    
    def clear_current_poi(self):
        """Clear the current POI"""
        self.current_poi = None
        print("Current POI cleared")
    
    def clear_history(self):
        """Clear POI history"""
        self.poi_history = []
        print("POI history cleared")
    
    def export_poi_data(self, format_type: str = 'json') -> str:
        """Export POI data in requested format"""
        if not self.current_poi:
            return ""
        
        if format_type == 'json':
            return json.dumps(self.current_poi, indent=2)
        elif format_type == 'simple':
            # User's requested format: x:10,y:50,r:300,tx="text"
            x = self.current_poi['x']
            y = self.current_poi['y']
            r = self.current_poi['radius']
            tx = self.current_poi['text']
            return f'x:{x},y:{y},r:{r},tx="{tx}"'
        elif format_type == 'coordinates_only':
            return f"({self.current_poi['x']}, {self.current_poi['y']})"
        else:
            return str(self.current_poi)
    
    def has_poi(self) -> bool:
        """Check if there's a current POI"""
        return self.current_poi is not None
    
    def get_poi_age(self) -> Optional[float]:
        """Get age of current POI in seconds"""
        if self.current_poi:
            return time.time() - self.current_poi['timestamp']
        return None
    
    def is_poi_recent(self, max_age_seconds: int = 300) -> bool:
        """Check if current POI is recent (within max_age_seconds)"""
        age = self.get_poi_age()
        return age is not None and age <= max_age_seconds 