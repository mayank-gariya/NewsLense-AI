import spacy
from app.utils.logger import logger

class NLPManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            logger.info("Loading spaCy model...")
            
            cls._instance = super().__new__(cls)
            cls._instance.nlp = spacy.load("en_core_web_sm")

            logger.info("✓ spaCy loaded.")

        return cls._instance

    def process(self, text: str):

        return self.nlp(text)