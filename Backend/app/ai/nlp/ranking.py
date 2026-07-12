from app.ai.nlp.stopwords import STOP_KEYWORDS


class KeywordRanker:

    ENTITY_WEIGHTS = {
        "ORG": 0.40,
        "PRODUCT": 0.35,
        "PERSON": 0.25,
        "GPE": 0.20,
        "LOC": 0.20,
        "EVENT": 0.20,
        "FAC": 0.15,
        "NORP": 0.15,
        "DATE": 0.05,
        "TIME": 0.05,
        "MONEY": 0.05
    }

    def boost_entities(
        self,
        keywords,
        entities
    ):

        entity_map = {
            entity["text"].lower(): entity["label"]
            for entity in entities
        }

        ranked = []

        for keyword in keywords:

            score = keyword["score"]
            label = entity_map.get(
                keyword["text"].lower()
            )

            if label:
                score -= self.ENTITY_WEIGHTS.get(
                    label,
                    0.10
                )
                
                keyword['metadata'] = {
                    'source':'NER + YAKE',
                    'entity':label
                }
            else:
                keyword['metadata'] = {
                    'source':'YAKE'
                } 
                
            ranked.append({
                "text": keyword["text"],
                "score": round(score,4),
                'metadata':keyword['metadata']
            })

        ranked.sort(
            key=lambda x: x["score"]
        )

        return ranked

    def remove_noise(
        self,
        keywords
    ):

        return [
            keyword
            for keyword in keywords
            if keyword["text"].lower()
            not in STOP_KEYWORDS

        ]

    def deduplicate(
        self,
        keywords
    ):

        seen = set()
        result = []

        for keyword in keywords:
            key = keyword["text"].lower()
            if key in seen:
                continue
            seen.add(key)
            result.append(keyword)

        return result