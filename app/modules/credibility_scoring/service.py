import re
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from .repository import CredibilityScoreRepository
from .schema import ArgumentInput, ScoreOutput


class CredibilityScoringService:
    def __init__(self):
        self.repo = CredibilityScoreRepository()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_cache = {}

    def score_argument(self, data: ArgumentInput):
        relevance = self.calculate_relevance(data.text, data.debate_id)
        evidence, evidence_notes = self.calculate_evidence(data.text)
        consistency = self.calculate_consistency(
            data.participant_id, data.text, data.debate_id
        )
        overall = float((relevance + evidence + consistency) / 3.0)
        notes = f"{evidence_notes}" if evidence_notes else None
        self.repo.save_score(
            data.argument_id,
            data.participant_id,
            relevance,
            evidence,
            consistency,
            overall,
            notes,
        )
        return ScoreOutput(
            argument_id=data.argument_id,
            participant_id=data.participant_id,
            relevance_score=relevance,
            evidence_score=evidence,
            consistency_score=consistency,
            overall_strength=overall,
            notes=notes,
        )

    def calculate_relevance(self, text: str, debate_id: int):
        debate_topic = self._get_debate_topic(debate_id)
        if debate_topic:
            topic_embd = self._embed(debate_topic)
            text_embd = self._embed(text)
            sim = self.model.similarity(topic_embd, text_embd)
            score = float((sim + 1) / 2)
            return max(0.0, min(1.0, score))
        return 0

    def calculate_evidence(self, text: str):
        notes = []

        if re.search(r"\d{2,}", text):
            notes.append("contains numbers")

        if re.search(r"https?://|doi:|arxiv:", text, re.I):
            notes.append("contains url/source")

        if re.search(r"\b(study|research|according to|reported|survey)\b", text, re.I):
            notes.append("mentions research/literature")

        if re.search(r"\([A-Za-z]+, \d{4}\)", text):
            notes.append("citation-style mention")

        evidence_score = 0.0
        if notes:
            evidence_score = min(1.0, 0.4 + 0.2 * len(notes))
        else:
            # look for reasoning connectors (because, therefore)
            if re.search(r"\b(because|therefore|hence|thus|since)\b", text, re.I):
                evidence_score = 0.5
            else:
                evidence_score = 0.2
        return float(evidence_score), "; ".join(notes)

    def calculate_consistency(
        self, participant_id: int, text: str, debate_id: int
    ) -> float:
        prev_texts = self._get_participant_previous_arguments(participant_id, debate_id)
        if not prev_texts:
            return 0.8
        emb_text = self._embed(text)
        sims = []
        for pt in prev_texts:
            emb_pt = self._embed(pt)
            sims.append(self._cosine_sim(emb_text, emb_pt))
        avg_sim = np.mean(sims) if sims else 0.0
        # normalize from (-1..1) to (0..1)
        score = float((avg_sim + 1) / 2)
        # if text contradicts earlier explicit stance detection could lower score (optional)
        return max(0.0, min(1.0, score))

    def _cosine_sim(self, a, b):
        a = a / np.linalg.norm(a) if np.linalg.norm(a) != 0 else a
        b = b / np.linalg.norm(b) if np.linalg.norm(b) != 0 else b
        return float(np.dot(a, b))

    def _embed(self, text: str):
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        embd = self.model.encode(text, convert_to_numpy=True)
        self.embedding_cache[text] = embd
        return embd

    def _get_debate_topic(self, debate_id: int) -> str:
        from database.models.debates import Debates

        db = self.repo.db
        debate = db.query(Debates).filter(Debates.id == debate_id).first()
        print(debate)
        return debate.title if debate else ""

    def _get_participant_previous_arguments(
        self, participant_id: int, debate_id: int
    ) -> List[str]:
        from database.models.arguments import Arguments

        db = self.repo.db
        rows = (
            db.query(Arguments.content)
            .filter(
                Arguments.user_id == participant_id, Arguments.debate_id == debate_id
            )
            .order_by(Arguments.created_at.asc())
            .all()
        )
        return [r[0] for r in rows]
