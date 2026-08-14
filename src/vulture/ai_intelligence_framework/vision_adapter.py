"""Vision model adapter."""
import logging
logger = logging.getLogger(__name__)
class VisionAdapter:
    def __init__(self, model_name='clip'):
        self.model_name = model_name
        self.model = None
    def load_model(self):
        try:
            if self.model_name == 'clip':
                import clip
                self.model = clip.load('ViT-B/32')
                logger.info("CLIP model loaded")
        except:
            logger.warning("Failed to load vision model")
    def encode_image(self, image):
        if self.model:
            return self.model.encode_image(image)
        return None
    def encode_text(self, text):
        if self.model:
            return self.model.encode_text(text)
        return None