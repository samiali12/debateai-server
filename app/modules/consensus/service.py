from typing import List, Dict, Any
from .repository import ConsensusRepository
from .schemas import ConsensusResponse, SideSummary, RecommendationItem
from datetime import datetime
import math
import re
from core.logger import logger


class ConsensusService:
    def __init__(self):
        self.repo = ConsensusRepository()

    @staticmethod
    def _clean_text(s: str) -> str:
        if not s:
            return ""
        return re.sub(r"\s+", " ", s).strip()

    def _concat_messages(self, items: List[Dict[str, Any]], max_chars: int = 3000) -> str:
        texts = [self._clean_text(i["content"]) for i in items]
        joined = "\n".join(texts)
        if len(joined) > max_chars:
            return joined[: max_chars - 200] + "\n...\n" + joined[-200:]
        return joined

    def summarize_side(self, debate_id: int, role: str) -> SideSummary:
        items = self.repo.get_messages_by_debate_and_role(debate_id, role)
        combined_text = self._concat_messages(items)

        if not combined_text:
            return SideSummary(role=role, summary="", top_points=[])

        # Rule-based summary:
        # Step 1 → pick first 3 meaningful sentences
        sentences = re.split(r"(?<=[.!?])\s+", combined_text)
        filtered = [s.strip() for s in sentences if len(s.strip()) > 10]

        summary = " ".join(filtered[:3])
        if len(summary) > 450:
            summary = summary[:450] + "..."

        top_points = filtered[:3]

        return SideSummary(role=role, summary=summary, top_points=top_points)

    def _find_shared_goals_and_conflicts(self, for_summary: str, against_summary: str):
        def tokenize(s):
            s = re.sub(r"[^\w\s]", "", s.lower())
            return set([w for w in s.split() if len(w) > 3])

        fset = tokenize(for_summary)
        aset = tokenize(against_summary)

        shared = sorted(list(fset.intersection(aset)))[:8]
        conflicts = sorted(list((fset.union(aset) - fset.intersection(aset))))[:8]

        return {"shared_goals": shared, "top_conflicts": conflicts}

    def _rule_based_recommendations(
        self, shared_goals, top_conflicts, for_summary, against_summary
    ):
        recommendations = []

        # Rule 1: Shared goals → emphasize cooperation
        if shared_goals:
            recommendations.append({
                "type": "shared_goal_alignment",
                "text": f"Both sides highlight shared goals such as {', '.join(shared_goals)}. Focusing on these points may help build agreement.",
                "confidence": 0.85,
                "fairness": 0.9,
                "feasibility": 0.9,
            })

        # Rule 2: Conflicts → suggest compromise
        if top_conflicts:
            recommendations.append({
                "type": "conflict_resolution",
                "text": f"The debate includes differing views around: {', '.join(top_conflicts)}. A balanced resolution may involve acknowledging these concerns and proposing a compromise.",
                "confidence": 0.8,
                "fairness": 0.85,
                "feasibility": 0.75,
            })

        # Rule 3: Question marks imply misunderstandings
        if "?" in for_summary or "?" in against_summary:
            recommendations.append({
                "type": "clarity_and_tone",
                "text": "Some uncertainties were raised in the discussion. Clarifying key assumptions may help reduce confusion.",
                "confidence": 0.75,
                "fairness": 0.8,
                "feasibility": 0.8,
            })

        # Fallback
        if not recommendations:
            recommendations.append({
                "type": "general",
                "text": "No strong agreements or conflicts detected. A structured list of priorities or key issues may help guide the debate forward.",
                "confidence": 0.7,
                "fairness": 0.75,
                "feasibility": 0.7,
            })

        return recommendations

    @staticmethod
    def _score_text_quality(text: str) -> float:
        if not text or len(text.strip()) < 20:
            return 0.2

        score = min(1.0, math.log(len(text) + 1) / 6.0)
        return float(round(score, 3))

    def generate_consensus(self, debate_id: int, save: bool = True) -> ConsensusResponse:

        # Summaries
        for_summary = self.summarize_side(debate_id, "for")
        against_summary = self.summarize_side(debate_id, "against")

        # If both are empty → fallback: split messages
        if not for_summary.summary and not against_summary.summary:
            all_msgs = self.repo.get_all_messages_by_debate(debate_id)
            mid = len(all_msgs) // 2
            for_text = self._concat_messages(all_msgs[:mid])
            against_text = self._concat_messages(all_msgs[mid:])

            for_summary.summary = for_text[:450] + "..."
            against_summary.summary = against_text[:450] + "..."

        # Shared goals & conflicts
        shared_info = self._find_shared_goals_and_conflicts(
            for_summary.summary, against_summary.summary
        )
        shared_goals = shared_info["shared_goals"]
        top_conflicts = shared_info["top_conflicts"]

        # Recommendations (RULE-BASED)
        recs_raw = self._rule_based_recommendations(
            shared_goals, top_conflicts, for_summary.summary, against_summary.summary
        )

        # Convert recommendations → RecommendationItem
        rec_items = []
        for r in recs_raw:
            text = r["text"]
            typ = r["type"]

            # compute fairness score
            fairness = (
                len([w for w in shared_goals if w in text.lower()])
                / max(1, len(shared_goals))
                if shared_goals else 0.5
            )
            fairness = float(round(min(max(fairness, 0.0), 1.0), 3))

            quality = self._score_text_quality(text)
            feasibility = r["feasibility"]
            confidence = float(round((quality * fairness * feasibility) ** (1 / 3), 3))

            rec_items.append(
                RecommendationItem(
                    id=None,
                    text=text,
                    type=typ,
                    confidence=confidence,
                    fairness=fairness,
                    feasibility=feasibility,
                )
            )

        # Final response payload
        payload = {
            "debate_id": debate_id,
            "generated_at": datetime.utcnow().isoformat(),
            "for_summary": for_summary.dict(),
            "against_summary": against_summary.dict(),
            "shared_goals": shared_goals,
            "top_conflicts": top_conflicts,
            "recommendations": [r.dict() for r in rec_items],
        }

        # Save to DB
        saved = None
        if save:
            summary_text = (rec_items[0].text[:400] + "...") if rec_items else ""
            saved = self.repo.save_recommendation(debate_id, payload, summary_text)

            # attach fake ids for response
            if saved and hasattr(saved, "id"):
                for i, r in enumerate(rec_items):
                    r.id = saved.id * 1000 + i

        return ConsensusResponse(
            debate_id=debate_id,
            generated_at=datetime.utcnow(),
            for_summary=for_summary,
            against_summary=against_summary,
            shared_goals=shared_goals,
            top_conflicts=top_conflicts,
            recommendations=rec_items,
        )

    def get_latest_consensus(self, debate_id: int) -> Dict[str, Any]:
        rec = self.repo.get_latest_recommendation(debate_id)
        if not rec:
            return {}
        return rec.payload
