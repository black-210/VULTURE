"""Metadata extraction from IQ files."""
import json
import logging
logger = logging.getLogger(__name__)
class MetadataExtractor:
    def __init__(self):
        self.metadata = {}
    def extract_from_file(self, filename):
        meta_file = filename + '.json'
        try:
            with open(meta_file, 'r') as f:
                self.metadata = json.load(f)
            return self.metadata
        except:
            return {}
    def save_metadata(self, filename, metadata):
        meta_file = filename + '.json'
        try:
            with open(meta_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            return False
    def get_metadata_field(self, field):
        return self.metadata.get(field)
    def set_metadata_field(self, field, value):
        self.metadata[field] = value