from transformers import pipeline
from modules.summerization.repository import SummerizationRepository
from modules.arguments.service import ArgumentService
from modules.argument_segmentation.service import ArgumentSegmentationService


class SummerizationService:

    def __init__(self):
        self.arguments = ArgumentService()
        self.segmentation = ArgumentSegmentationService()
        self.repo = SummerizationRepository()
        self.summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            tokenizer="sshleifer/distilbart-cnn-12-6",
            device=-1,
        )

    def generate_summary(self, debate_id: int) -> str:
        arguments_list = self.arguments.get_arguments(debate_id)
        arguments_content = [arg["content"] for arg in arguments_list.data]
        segmentations_list = [
            self.segmentation.segment_arguments(arg) for arg in arguments_content
        ]

        all_segments = []
        for seg in segmentations_list:
            all_segments.extend(seg)

        role_segment_pairs = []
        for arg, segs in zip(arguments_list.data, segmentations_list):
            for seg in segs:
                role_segment_pairs.append({"text": seg, "role": arg["role"]})

        pros = [
            item["text"] for item in role_segment_pairs if item["role"].value == "for"
        ]
        cons = [
            item["text"]
            for item in role_segment_pairs
            if item["role"].value == "against"
        ]
        neutral = [
            item["text"]
            for item in role_segment_pairs
            if item["role"].value == "neutral"
        ]

        def summarize_segments(segments: str):
            if not segments:
                return {"summary_text": "No point is provided."}

            combined_text = " ".join(segments)

            summary = self.summarizer(
                combined_text,
                max_length=130,
                min_length=30,
                num_beams=4,
                length_penalty=1.0,
            )
            return summary[0]["summary_text"]

        return {
            "pros": summarize_segments(pros),
            "cons": summarize_segments(cons),
            "neutral": summarize_segments(neutral),
        }
