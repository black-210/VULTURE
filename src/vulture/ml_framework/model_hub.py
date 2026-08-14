"""Model hub for managing trained models."""
import pickle
import json
import logging
logger = logging.getLogger(__name__)
class ModelHub:
    def __init__(self, model_dir='./models'):
        self.model_dir = model_dir
        self.models = {}
    def save_model(self, model, name, metadata=None):
        path = f"{self.model_dir}/{name}.pkl"
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        if metadata:
            with open(f"{self.model_dir}/{name}_meta.json", 'w') as f:
                json.dump(metadata, f)
        logger.info(f"Model saved: {name}")
    def load_model(self, name):
        path = f"{self.model_dir}/{name}.pkl"
        with open(path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded: {name}")
        return model
    def list_models(self):
        import os
        return [f.replace('.pkl', '') for f in os.listdir(self.model_dir) if f.endswith('.pkl')]
    def get_model_metadata(self, name):
        try:
            with open(f"{self.model_dir}/{name}_meta.json", 'r') as f:
                return json.load(f)
        except:
            return {}