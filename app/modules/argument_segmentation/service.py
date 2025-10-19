import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class ArgumentSegmentationService:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))

    def text_processing(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s.,?!]", "", text)
        tokens = word_tokenize(text)
        filtered = [t for t in tokens if t not in self.stop_words]
        return filtered

    def segment_arguments(self, text: str):
        sentences = sent_tokenize(text)
        return [s.strip() for s in sentences if s.strip()]
