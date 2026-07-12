import yake

from app.ai.nlp.preprocessing import TextPreprocessor
from app.ai.nlp.ner import NamedEntityRecognizer
from app.ai.nlp.ranking import KeywordRanker

class KeywordExtractor:
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.extractor = yake.KeywordExtractor(
            lan='en',
            n=2,
            dedupLim=0.85,
            dedupFunc="seqm",
            windowsSize=2,
            top=15
        )
        self.ner = NamedEntityRecognizer()
        self.ranker = KeywordRanker()
        
    def extract(
        self,
        text: str
    ):

        if not text:
            return []

        clean_text = self.preprocessor.get_clean_text(
            text
        )

        keywords = [
            {
                "text": keyword,
                "score": round(score,4),
                'metadata':{
                    'source':'YAKE'
                }
            }
            for keyword, score in
            self.extractor.extract_keywords(
                clean_text
            )
        ]

        entities = self.ner.extract(text)

        keywords = self.ranker.boost_entities(
            keywords,
            entities
        )

        keywords = self.ranker.remove_noise(
            keywords
        )

        keywords = self.ranker.deduplicate(
            keywords
        )

        return keywords