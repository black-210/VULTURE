"""LLM Router for multiple AI models."""
import logging
logger = logging.getLogger(__name__)
class LLMRouter:
    def __init__(self, default_model='local'):
        self.default_model = default_model
        self.models = {'local': None, 'openai': None, 'custom': None}
    def set_model(self, model_name, model_instance):
        self.models[model_name] = model_instance
    def query(self, prompt, model=None):
        model = model or self.default_model
        if self.models[model] is None:
            logger.error(f"Model {model} not initialized")
            return None
        return self.models[model].query(prompt)
    def get_available_models(self):
        return [m for m in self.models if self.models[m] is not None]