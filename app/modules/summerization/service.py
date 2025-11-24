import io
from time import time
from transformers import pipeline
from core.supabase import upload_pdf_to_supabase
from modules.summerization.repository import SummerizationRepository
from modules.arguments.service import ArgumentService
from modules.argument_segmentation.service import ArgumentSegmentationService
from modules.debates.service import DebateService
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from core.logger import logger


class SummerizationService:

    def __init__(self):
        self.arguments = ArgumentService()
        self.segmentation = ArgumentSegmentationService()
        self.repo = SummerizationRepository()
        self.debate_service = DebateService()
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

        res_data = {
            "pros": summarize_segments(pros),
            "cons": summarize_segments(cons),
            "neutral": summarize_segments(neutral)["summary_text"],
        }

        public_url = self.generate_pdf_report(debate_id, res_data)
        self.repo.create_summary(debate_id=debate_id, url=public_url)

        return res_data

    def generate_pdf_report(self, debate_id: int, data: dict) -> str:

        try:
            logger.info(f"📄 Generating PDF report for debate {debate_id}")

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            elements = []

            # Add content to PDF
            styles = getSampleStyleSheet()
            normal = styles["Normal"]
            heading = styles["Heading2"]

            elements.append(
                Paragraph(f"Debate Summary (ID: {debate_id})", styles["Heading1"])
            )
            elements.append(Spacer(1, 16))

            elements.append(Paragraph("Arguments For:", heading))
            elements.append(Paragraph(data.get("pros", ""), normal))
            elements.append(Spacer(1, 12))

            # Cons
            elements.append(Paragraph("Arguments Against:", heading))
            elements.append(Paragraph(data.get("cons", ""), normal))
            elements.append(Spacer(1, 12))

            # Neutral
            elements.append(Paragraph("Neutral Points:", heading))
            elements.append(Paragraph(data.get("neutral", ""), normal))
            elements.append(Spacer(1, 12))

            # Build PDF
            doc.build(elements)

            # Reset buffer position
            buffer.seek(0)

            # Generate file name
            file_name = f"debate_summary_{debate_id}_{int(time())}.pdf"

            # Upload to Supabase with error handling
            try:
                public_url = upload_pdf_to_supabase(buffer.getvalue(), file_name)
                logger.info(f"✅ PDF report generated and uploaded: {public_url}")
                return public_url
            except Exception as upload_error:
                logger.error(f"❌ Failed to upload PDF: {upload_error}")
                # Fallback: save locally for debugging
                local_path = f"debug_{file_name}"
                with open(local_path, "wb") as f:
                    f.write(buffer.getvalue())
                logger.info(f"💾 PDF saved locally for debugging: {local_path}")
                raise

        except Exception as e:
            logger.error(f"❌ PDF generation failed: {str(e)}")
            raise

    def get_summary(self, debate_id: int):
        return self.repo.get_summary(debate_id=debate_id)
