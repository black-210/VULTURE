"""CLIP-based vision model integration."""

import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

HAS_CLIP = False
try:
    import clip
    import torch
    HAS_CLIP = True
except ImportError:
    pass


class VisionAdapter:
    """Vision-language model adapter (CLIP)."""

    def __init__(self, model_name: str = 'ViT-B/32'):
        """
        Args:
            model_name: CLIP model name
        """
        if not HAS_CLIP:
            logger.warning("CLIP not installed. Install: pip install clip-torch")
            self.model = None
            self.preprocess = None
            self.device = None
        else:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model, self.preprocess = clip.load(model_name, device=self.device)
            logger.info(f"✓ Loaded CLIP model: {model_name}")

    def encode_image(self, image_path: str) -> np.ndarray:
        """Encode image to embedding.
        
        Args:
            image_path: Path to image
            
        Returns:
            Image embedding
        """
        if not HAS_CLIP or self.model is None:
            raise RuntimeError("CLIP not available")
        
        try:
            from PIL import Image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                embedding = self.model.encode_image(image_tensor)
            
            return embedding.cpu().numpy()[0]
        except Exception as e:
            logger.error(f"Image encoding failed: {e}")
            raise

    def encode_text(self, text: str) -> np.ndarray:
        """Encode text to embedding.
        
        Args:
            text: Input text
            
        Returns:
            Text embedding
        """
        if not HAS_CLIP or self.model is None:
            raise RuntimeError("CLIP not available")
        
        text_tensor = clip.tokenize(text).to(self.device)
        
        with torch.no_grad():
            embedding = self.model.encode_text(text_tensor)
        
        return embedding.cpu().numpy()[0]

    def similarity(self, image_embedding: np.ndarray,
                  text_embedding: np.ndarray) -> float:
        """Compute image-text similarity.
        
        Args:
            image_embedding: Image embedding
            text_embedding: Text embedding
            
        Returns:
            Cosine similarity
        """
        from sklearn.metrics.pairwise import cosine_similarity
        return float(cosine_similarity([image_embedding], [text_embedding])[0][0])
