from app.ai.inference.summarizer import Summarizer
from app.ai.inference.sentiment import SentimentInference
from app.ai.inference.topic_classifier import TopicClassifier
from app.ai.nlp.ner import NamedEntityRecognizer
from app.ai.nlp.keyword_extractor import KeywordExtractor
from app.ai.inference.question_answering import QuestionAnswering

class AIService:

    def __init__(self):
        self.summarizer = Summarizer()
        self.sentiment = SentimentInference()
        self.topic_classifier = TopicClassifier()
        self.ner = NamedEntityRecognizer()
        self.keyword_extractor = KeywordExtractor()
        self.question_answering = QuestionAnswering()
        
    def generate_summary(
        self,
        text: str
    ):
        if not text:
            return []
        
        text = text.strip()
                
        # Prevent transformer errors on very short text
        if len(text.split()) < 50:
            return text

        return self.summarizer.summarize(text)
    
    def analyze_sentiment(self,text:str):
        if not text:
            return []
        
        short_text = self._prepare_short_text(text)
        return self.sentiment.analyze(short_text)
    
    def classify_topic(self,text:str):
        if not text:
            return []
        
        short_text = self._prepare_short_text(text)
        return self.topic_classifier.classify(short_text)
    
    def extract_entities(self,text:str):
        if not text:
            return []
        
        short_text = self._prepare_short_text(text)
        return self.ner.extract(short_text)
    
    def extract_keywords(self,text:str):      
        
        short_text = self._prepare_short_text(text)
        return self.keyword_extractor.extract(short_text)
   
    def answer_question(
        self,
        question: str,
        context: str
    ):

        if not question:
            return None

        if not context:
            return None

        context = context.strip()

        return self.question_answering.answer(
            question=question,
            context=context
        )
        
    def _prepare_short_text(self, text: str) -> str:
        """
        Limit text length for transformer models
        """
        return " ".join(text.split()[:450])