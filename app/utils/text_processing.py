import re

def preprocess_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9,.!?;:\'\"()\-\s]', '', text)
    return text

def segment_text(text: str) -> list[str]:
    """Simple rule-based segmentation by punctuation and conjunctions."""
    # split on sentence delimiters
    parts = re.split(r'[.!?]+', text)
    segments = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # further split by conjunctions for smaller argument units
        subparts = re.split(r'\b(because|and|but|so|although|since|however)\b', part)
        subparts = [s.strip() for s in subparts if s.strip()]
        segments.extend(subparts)
    return segments

def process_text(text: str) -> dict:
    clean_text = preprocess_text(text)
    segments = segment_text(clean_text)
    return {
        "original_text": text,
        "segments": segments
    }