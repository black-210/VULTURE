"""Conversation memory with max-size limits."""

import logging
from typing import List, Dict
from collections import deque

logger = logging.getLogger(__name__)


class MemoryManager:
    """Conversation memory buffer."""

    def __init__(self, max_memory_size: int = 100, max_tokens: int = 10000):
        """
        Args:
            max_memory_size: Max number of messages
            max_tokens: Max token count (approximate)
        """
        self.max_memory_size = max_memory_size
        self.max_tokens = max_tokens
        self.memory: deque = deque(maxlen=max_memory_size)
        self.token_count = 0

    def add_message(self, role: str, content: str) -> None:
        """Add message to memory.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        message = {'role': role, 'content': content}
        tokens = len(content.split())  # Rough estimate
        
        # Check memory constraints
        if len(self.memory) >= self.max_memory_size:
            old_msg = self.memory.popleft()
            self.token_count -= len(old_msg['content'].split())
        
        if self.token_count + tokens > self.max_tokens:
            # Remove oldest messages until under limit
            while self.memory and self.token_count + tokens > self.max_tokens:
                old_msg = self.memory.popleft()
                self.token_count -= len(old_msg['content'].split())
        
        self.memory.append(message)
        self.token_count += tokens
        logger.debug(f"Memory: {len(self.memory)} messages, {self.token_count} tokens")

    def get_context(self, max_messages: int = None) -> List[Dict]:
        """Get conversation context.
        
        Args:
            max_messages: Limit number of messages
            
        Returns:
            List of messages
        """
        messages = list(self.memory)
        if max_messages:
            messages = messages[-max_messages:]
        return messages

    def clear(self) -> None:
        """Clear memory."""
        self.memory.clear()
        self.token_count = 0
        logger.info("Memory cleared")

    def get_summary_stats(self) -> Dict:
        """Get memory statistics.
        
        Returns:
            Memory stats dict
        """
        return {
            'num_messages': len(self.memory),
            'token_count': self.token_count,
            'max_memory_size': self.max_memory_size,
            'max_tokens': self.max_tokens,
            'occupancy_percent': 100 * self.token_count / self.max_tokens,
        }
