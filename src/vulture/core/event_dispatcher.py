"""Event-Driven Architecture

Publish-subscribe event system.
"""

from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class Event:
    """Event object"""
    type: str
    source: str
    timestamp: datetime
    data: Dict[str, Any]


class EventDispatcher:
    """Event dispatch system"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.logger = logging.getLogger("vulture.events")
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        self.logger.debug(f"Subscribed to {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from event type"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
    
    def publish(self, event: Event) -> None:
        """Publish event"""
        self.event_history.append(event)
        
        if event.type in self.subscribers:
            for callback in self.subscribers[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    self.logger.error(f"Error in event callback: {e}")
    
    def get_event_history(self) -> List[Event]:
        """Get event history"""
        return self.event_history.copy()
