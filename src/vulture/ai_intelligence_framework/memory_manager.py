"""Memory and context management."""
import logging
logger = logging.getLogger(__name__)
class MemoryManager:
    def __init__(self, max_memory=1000):
        self.max_memory = max_memory
        self.memory = []
    def add_memory(self, key, value):
        self.memory.append({'key': key, 'value': value})
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)
    def retrieve_memory(self, key):
        for item in self.memory:
            if item['key'] == key:
                return item['value']
        return None
    def clear_memory(self):
        self.memory = []
    def get_memory_stats(self):
        return {'size': len(self.memory), 'max_size': self.max_memory}