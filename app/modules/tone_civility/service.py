from transformers import pipeline
from .schemas import ToneCivilityResponse
from .repository import ToneCivilityRepository


class ToneCivilityService:
    def __init__(self):
        self.repo = ToneCivilityRepository()
        self.detector = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            tokenizer="unitary/toxic-bert",
            device=-1,  # CPU
        )

    def analyze_tone_civility(self, argument_id: int, text: str) -> dict:
        results = self.detector(text, truncation=True)
        toxicity_score = max(
            [res["score"] for res in results if res["label"].lower() != "non-toxic"]
        )
        civility_score = 1 - toxicity_score
        flag = None
        for res in results:
            if res["label"].lower() == "toxic" and res["score"] > 0.5:
                flag = "toxic"
                break
            else:
                flag = "civil"

        self.repo.save_analysis(
            argument_id=argument_id,
            toxicity_score=toxicity_score,
            civility_score=civility_score,
            flags=flag,
        )

        return ToneCivilityResponse(
            toxicity_score=toxicity_score,
            civility_score=civility_score,
            flags=flag,
        )
