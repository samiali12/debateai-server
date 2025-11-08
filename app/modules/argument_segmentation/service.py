import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

nltk_resources = {
    "punkt": "tokenizers/punkt",
    "stopwords": "corpora/stopwords",
    "wordnet": "corpora/wordnet",
}

for pkg, resource in nltk_resources.items():
    try:
        nltk.data.find(resource)
    except LookupError:
        # download quietly and only when resource is missing
        nltk.download(pkg, quiet=True)


class ArgumentSegmentationService:

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"http\S+|www\S+", "", text)
        text = re.sub(r"[^a-z\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def preprocess(self, text: str) -> list[str]:
        cleaned = self.clean_text(text)
        tokens = word_tokenize(cleaned)
        filtered = [
            self.lemmatizer.lemmatize(word)
            for word in tokens
            if word not in self.stop_words
        ]
        return filtered

    def segment_arguments(self, text: str) -> list[str]:
        text = self.clean_text(text)
        sentences = sent_tokenize(text)

        segments = []
        buffer = ""

        for sentence in sentences:
            buffer = sentence.strip() + " "

            if re.search(
                r"\b(because|however|therefore|although|but)\b", sentence.lower()
            ):
                segments.append(buffer.strip())
                buffer = ""

        if buffer:
            segments.append(buffer.strip())

        return segments
