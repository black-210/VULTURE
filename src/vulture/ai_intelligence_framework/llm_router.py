"""Multi-model LLM routing: OpenAI, local, custom."""

import logging
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)


class LLMRouter:
    """Unified LLM interface with fallback chains."""

    def __init__(self, primary_model: str = 'gpt-3.5-turbo', fallback_models: List[str] = None):
        """
        Args:
            primary_model: Primary LLM model
            fallback_models: Fallback models if primary fails
        """
        self.primary_model = primary_model
        self.fallback_models = fallback_models or []
        self.model_chain = [primary_model] + self.fallback_models
        self.temperature = 0.7
        self.max_tokens = 2048

    def route_request(self, prompt: str, system_prompt: str = None,
                     temperature: float = None) -> Dict:
        """Route request through model chain.
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Sampling temperature
            
        Returns:
            Response dict
        """
        if temperature is None:
            temperature = self.temperature
        
        # Try each model in chain
        for model in self.model_chain:
            try:
                response = self._query_model(model, prompt, system_prompt, temperature)
                logger.info(f"✓ Used model: {model}")
                return response
            except Exception as e:
                logger.warning(f"✗ Model {model} failed: {e}, trying fallback...")
                continue
        
        raise RuntimeError("All models in chain failed")

    def _query_model(self, model: str, prompt: str, system_prompt: str,
                    temperature: float) -> Dict:
        """Query specific model."""
        try:
            if 'gpt' in model.lower():
                return self._query_openai(model, prompt, system_prompt, temperature)
            elif 'local' in model.lower():
                return self._query_local(model, prompt)
            else:
                return self._query_custom(model, prompt)
        except Exception as e:
            raise RuntimeError(f"Query failed: {e}")

    def _query_openai(self, model: str, prompt: str, system_prompt: str,
                     temperature: float) -> Dict:
        """Query OpenAI API."""
        try:
            import openai
        except ImportError:
            raise ImportError("openai library required: pip install openai")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=self.max_tokens
        )
        
        return {
            'model': model,
            'response': response['choices'][0]['message']['content'],
            'tokens_used': response['usage']['total_tokens'],
        }

    def _query_local(self, model: str, prompt: str) -> Dict:
        """Query local model (placeholder)."""
        logger.info(f"Using local model: {model}")
        return {'model': model, 'response': f"Local model response to: {prompt[:50]}..."}

    def _query_custom(self, model: str, prompt: str) -> Dict:
        """Query custom model endpoint."""
        logger.info(f"Using custom model: {model}")
        return {'model': model, 'response': f"Custom model response: {prompt[:50]}..."}
