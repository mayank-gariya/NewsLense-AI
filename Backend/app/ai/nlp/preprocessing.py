import re

from app.ai.nlp.manager import NLPManager

class TextPreprocessor:
    def __init__(self):
        self.nlp = NLPManager()
        
    def clean_text(self,text:str):
        if not text:
            return None
        text = re.sub(r'<.*?>',' ',text)
        text = re.sub(r'\s+',' ',text)
        
        return text.strip()
    
    def process(self,text:str):
        cleaned = self.clean_text(text)
        
        return self.nlp.process(cleaned)
    
    def get_clean_text(self, text: str) -> str:
        return self.clean_text(text)