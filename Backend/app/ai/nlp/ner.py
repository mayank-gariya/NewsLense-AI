from app.ai.nlp.preprocessing import TextPreprocessor

class NamedEntityRecognizer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
    
    def extract(self,text:str):
        if not text:
            return []
        
        doc = self.preprocessor.process(text)
        
        seen = set()
        entities = []
        
        for ent in doc.ents:
            key = (ent.text.lower(),ent.label_)
            
            if key in seen:
                continue
            
            seen.add(key)
            
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        return entities