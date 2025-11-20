from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from .repository import AiModeratorRepository


class AiModeratorService:
    def __init__(self):
        self.repo = AiModeratorRepository()
        self.detector = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            tokenizer="unitary/toxic-bert",
            device=-1,  # CPU
        )

        self.question_generator_tokenizer = AutoTokenizer.from_pretrained(
            "google/flan-t5-small"
        )
        self.question_generator_model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-small"
        )

    def analyze_text(self, text: str) -> dict:
        result = self.detector(text)[0]
        label = result["label"]
        score = result["score"]

        if label == "toxic" and score > 0.85:
            flag = "toxic"
            warning = "Your message appears harmful. Please rephrase respectfully."
        elif label == "toxic" and score > 0.45:
            flag = "warning"
            warning = "This message may sound harsh. Consider softening the tone."
        else:
            flag = "civil"
            warning = None

        return {
            "flag": flag,
            "toxicity_score": float(score),
            "message": text,
            "warning": warning,
        }

    def generate_next_question(self, topic: str, history: list[str]):
        prompt = f"Debate topic: {topic}. Generate one thoughtful, neutral question to move the debate forward."
        inputs = self.question_generator_tokenizer(
            prompt, return_tensors="pt", truncation=True
        )
        outputs = self.question_generator_model.generate(
            **inputs, max_length=50, num_beams=4
        )
        question = self.question_generator_tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )
        return question

    def check_fairness(self, for_count: int, against_count: int):
        diff = abs(for_count - against_count)
        if diff >= 3:
            if for_count > against_count:
                return {
                    "fair": False,
                    "message": "FOR side is dominating. Invite AGAINST side to speak.",
                }
            else:
                return {
                    "fair": False,
                    "message": "AGAINST side is dominating. Invite FOR side to respond.",
                }

        return {"fair": True, "message": "Both sides are contributing equally."}
