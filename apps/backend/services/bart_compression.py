# services/bart_compression.py - BART Text Compression Engine
from transformers import pipeline
import asyncio
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import re

class BARTCompressionEngine:
    """
    BART Compression Engine - Turns long, noisy text into fast, actionable summaries.

    Mission: Compression engine for job descriptions, resumes, and career insights.
    Never touches embeddings, vector search, or ML models.
    """

    def __init__(self):
        """Initialize BART compression engine"""
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                tokenizer="facebook/bart-large-cnn",
                device=-1  # CPU for now, can be configured for GPU
            )
            self.is_initialized = True
            print("✅ BART Compression Engine initialized successfully!")
        except Exception as e:
            print(f"⚠️ BART initialization failed: {e}")
            self.is_initialized = False

    async def compress_job_description(self, job_data: Dict[str, Any]) -> str:
        """
        Use Case 1: Job Description Compression
        Summarize job descriptions into 3-5 bullet points with key responsibilities, skills, and impact.

        Input: Full job description text
        Output: 3-5 bullet points
        """
        if not self.is_initialized:
            return self._fallback_job_summary(job_data)

        try:
            description = job_data.get('description', '')
            title = job_data.get('title', '')
            skills = job_data.get('skills', '')

            # Prepare input text for summarization
            input_text = f"Job Title: {title}\n\nDescription: {description}"
            if skills:
                input_text += f"\n\nRequired Skills: {skills}"

            # Limit input length for BART
            input_text = input_text[:1024]  # BART can handle up to ~1024 tokens

            # Generate summary asynchronously
            summary = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.summarizer(
                    input_text,
                    max_length=150,
                    min_length=50,
                    do_sample=False,
                    num_beams=4
                )[0]['summary_text']
            )

            # Convert to bullet points
            return self._format_as_bullet_points(summary, "job")

        except Exception as e:
            print(f"⚠️ BART job compression failed: {e}")
            return self._fallback_job_summary(job_data)

    async def compress_resume_to_recruiter_summary(self, resume_data: Dict[str, Any]) -> str:
        """
        Use Case 2: Resume → Recruiter Summary
        Convert parsed resume text into professional summary, highlighted skills, and experience snapshot.

        Input: Parsed resume data
        Output: Professional summary for employer dashboard
        """
        if not self.is_initialized:
            return self._fallback_resume_summary(resume_data)

        try:
            # Extract key sections
            summary = resume_data.get('summary', '')
            experience = resume_data.get('experience', [])
            skills = resume_data.get('skills', [])
            education = resume_data.get('education', [])

            # Build comprehensive input text
            input_parts = []
            if summary:
                input_parts.append(f"Professional Summary: {summary}")
            if experience:
                exp_text = "\n".join([f"- {exp.get('position', '')} at {exp.get('company', '')}: {exp.get('description', '')[:200]}" for exp in experience[:3]])
                input_parts.append(f"Experience: {exp_text}")
            if skills:
                skills_text = ", ".join(skills[:10])
                input_parts.append(f"Skills: {skills_text}")
            if education:
                edu_text = "\n".join([f"- {edu.get('degree', '')} from {edu.get('institution', '')}" for edu in education[:2]])
                input_parts.append(f"Education: {edu_text}")

            input_text = "\n\n".join(input_parts)
            input_text = input_text[:1024]

            # Generate summary
            summary = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.summarizer(
                    input_text,
                    max_length=120,
                    min_length=40,
                    do_sample=False,
                    num_beams=4
                )[0]['summary_text']
            )

            return self._format_recruiter_summary(summary)

        except Exception as e:
            print(f"⚠️ BART resume compression failed: {e}")
            return self._fallback_resume_summary(resume_data)

    async def compress_career_insights(self, insights_data: Dict[str, Any]) -> str:
        """
        Use Case 3: Career Insight Summaries
        Summarize market intelligence, trends, and salary insights into actionable insights.

        Input: Market intelligence text, trend analysis, salary insights
        Output: "What this means for you" summary with 2-3 concise insights
        """
        if not self.is_initialized:
            return self._fallback_career_insights(insights_data)

        try:
            market_text = insights_data.get('market_intelligence', '')
            trends = insights_data.get('trend_analysis', '')
            salary_info = insights_data.get('salary_insights', '')

            input_text = f"Market Intelligence: {market_text}\n\nTrend Analysis: {trends}\n\nSalary Insights: {salary_info}"
            input_text = input_text[:1024]

            # Generate summary
            summary = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.summarizer(
                    input_text,
                    max_length=100,
                    min_length=30,
                    do_sample=False,
                    num_beams=4
                )[0]['summary_text']
            )

            return self._format_career_insights(summary)

        except Exception as e:
            print(f"⚠️ BART career insights compression failed: {e}")
            return self._fallback_career_insights(insights_data)

    def _format_as_bullet_points(self, summary: str, context: str) -> str:
        """Convert summary text into structured bullet points"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', summary)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Group into 3-5 key points
        bullet_points = []
        current_point = ""

        for sentence in sentences[:5]:  # Limit to 5 points
            if len(current_point) + len(sentence) < 100:  # Keep points concise
                current_point += sentence + ". "
            else:
                if current_point:
                    bullet_points.append(f"• {current_point.strip()}")
                current_point = sentence + ". "

        if current_point:
            bullet_points.append(f"• {current_point.strip()}")

        # Ensure we have at least 3 points
        while len(bullet_points) < 3 and sentences:
            remaining = sentences[len(bullet_points):len(bullet_points)+1]
            if remaining:
                bullet_points.append(f"• {remaining[0].strip()}.")

        return "\n".join(bullet_points[:5])  # Max 5 bullets

    def _format_recruiter_summary(self, summary: str) -> str:
        """Format resume summary for recruiters"""
        # Structure as professional summary
        formatted = f"Professional Summary:\n{summary}\n\n"
        formatted += "Key Highlights:\n"
        formatted += self._format_as_bullet_points(summary, "resume")
        return formatted

    def _format_career_insights(self, summary: str) -> str:
        """Format career insights with actionable takeaways"""
        formatted = f"What this means for you:\n\n"
        formatted += self._format_as_bullet_points(summary, "career")
        return formatted

    def _fallback_job_summary(self, job_data: Dict[str, Any]) -> str:
        """Fallback job summary when BART fails"""
        title = job_data.get('title', 'Position')
        return f"""• Exciting opportunity as {title}
• Join innovative team in green energy sector
• Competitive compensation and growth potential
• Contribute to sustainable development goals"""

    def _fallback_resume_summary(self, resume_data: Dict[str, Any]) -> str:
        """Fallback resume summary"""
        return """Professional Summary:
Experienced professional with strong background in relevant field.

Key Highlights:
• Demonstrated expertise in key areas
• Proven track record of success
• Strong technical and soft skills"""

    def _fallback_career_insights(self, insights_data: Dict[str, Any]) -> str:
        """Fallback career insights"""
        return """What this means for you:
• Growing demand in sustainable sectors
• Competitive compensation opportunities
• Strong career growth potential"""