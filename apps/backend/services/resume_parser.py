# services/resume_parser.py - Advanced Resume Parsing & Skill Extraction
import spacy
import pdfplumber
import docx
import re
from typing import List, Dict, Any
import json
import os
from pathlib import Path
from datetime import datetime

class AdvancedResumeParser:
    def __init__(self):
        """Initialize the advanced resume parser with NLP capabilities"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ SpaCy model loaded successfully!")
        except OSError:
            print("⚠️ SpaCy model not found, downloading...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

        # Enhanced skill database with categories
        self.skill_database = {
            "programming": {
                "python": ["python", "django", "flask", "pandas", "numpy", "tensorflow", "pytorch"],
                "javascript": ["javascript", "react", "node.js", "angular", "vue", "typescript"],
                "java": ["java", "spring", "hibernate", "maven", "gradle"],
                "data_science": ["machine learning", "data analysis", "statistics", "sql", "r", "tableau"],
                "web_dev": ["html", "css", "bootstrap", "tailwind", "sass", "webpack"]
            },
            "renewable_energy": {
                "solar": ["solar", "photovoltaic", "pv", "solar panels", "solar energy"],
                "wind": ["wind", "wind turbine", "wind farm", "wind energy"],
                "hydro": ["hydro", "hydropower", "dam", "water turbine"],
                "geothermal": ["geothermal", "thermal energy", "heat pump"],
                "biomass": ["biomass", "biofuel", "renewable fuel"]
            },
            "engineering": {
                "mechanical": ["mechanical engineering", "cad", "solidworks", "autocad"],
                "electrical": ["electrical engineering", "power systems", "circuit design"],
                "civil": ["civil engineering", "construction", "structural design"],
                "environmental": ["environmental engineering", "waste management", "water treatment"]
            },
            "business": {
                "management": ["project management", "agile", "scrum", "leadership"],
                "analysis": ["business analysis", "requirements gathering", "stakeholder management"],
                "sustainability": ["esg", "sustainability reporting", "csr", "green finance"]
            }
        }

        # Experience level indicators
        self.experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
            r'(\d+)\s*years?\s*(?:of\s*)?(?:professional\s*)?experience',
        ]

        # Education level mapping
        self.education_levels = {
            "phd": ["phd", "ph.d", "doctorate", "doctoral"],
            "masters": ["masters", "master's", "msc", "ms", "ma", "m.tech", "m.e"],
            "bachelors": ["bachelors", "bachelor's", "bsc", "bs", "ba", "b.tech", "b.e"],
            "diploma": ["diploma", "certificate", "certification"]
        }

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF files with enhanced error handling"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"❌ PDF extraction error: {e}")
            return ""

    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from Word documents"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"❌ DOCX extraction error: {e}")
            return ""

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """Advanced skill extraction using NLP and pattern matching"""
        text_lower = text.lower()
        found_skills = {
            "technical": [],
            "domain": [],
            "soft": [],
            "certifications": []
        }

        # Extract technical skills
        for category, skills in self.skill_database.items():
            for skill_group, keywords in skills.items():
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        if category == "programming" or category == "engineering":
                            found_skills["technical"].append(skill_group.title())
                        elif category == "renewable_energy":
                            found_skills["domain"].append(skill_group.title())
                        elif category == "business":
                            found_skills["soft"].append(skill_group.title())

        # Remove duplicates
        found_skills["technical"] = list(set(found_skills["technical"]))
        found_skills["domain"] = list(set(found_skills["domain"]))
        found_skills["soft"] = list(set(found_skills["soft"]))

        # Extract certifications
        cert_patterns = [
            r'certified\s+([^,\n.]+)',
            r'certification\s+in\s+([^,\n.]+)',
            r'([^,\n.]+)\s+certification'
        ]

        for pattern in cert_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            found_skills["certifications"].extend([match.strip().title() for match in matches])

        found_skills["certifications"] = list(set(found_skills["certifications"]))

        return found_skills

    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience information using advanced pattern matching"""
        experience_info = {
            "years": 0,
            "level": "entry",
            "roles": [],
            "companies": []
        }

        # Extract years of experience
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    years = int(match)
                    if years > experience_info["years"]:
                        experience_info["years"] = years
                except ValueError:
                    continue

        # Determine experience level
        if experience_info["years"] >= 8:
            experience_info["level"] = "senior"
        elif experience_info["years"] >= 3:
            experience_info["level"] = "mid"
        else:
            experience_info["level"] = "entry"

        # Extract job roles and companies using NLP
        doc = self.nlp(text)
        potential_roles = []
        potential_companies = []

        for ent in doc.ents:
            if ent.label_ == "ORG":
                potential_companies.append(ent.text.strip())
            elif ent.label_ in ["JOB_TITLE", "WORK_OF_ART"]:
                if len(ent.text.split()) <= 4:  # Reasonable job title length
                    potential_roles.append(ent.text.strip())

        # Filter and clean
        experience_info["companies"] = list(set(potential_companies))[:5]  # Top 5
        experience_info["roles"] = list(set(potential_roles))[:5]

        return experience_info

    def extract_education(self, text: str) -> Dict[str, Any]:
        """Extract education information"""
        education_info = {
            "level": "bachelors",
            "degree": "",
            "field": "",
            "institution": ""
        }

        text_lower = text.lower()

        # Find highest education level
        for level, keywords in self.education_levels.items():
            for keyword in keywords:
                if keyword in text_lower:
                    education_info["level"] = level
                    education_info["degree"] = keyword.title()
                    break

        # Extract field of study using NLP
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORG" and any(word in ent.text.lower() for word in ["university", "college", "institute"]):
                education_info["institution"] = ent.text.strip()
                break

        return education_info

    def generate_skill_vector(self, skills: Dict[str, List[str]]) -> List[float]:
        """Generate skill vector for ML matching"""
        # Flatten all skills into a single list
        all_skills = []
        for category in skills.values():
            all_skills.extend(category)

        skill_text = " ".join(all_skills)
        if not skill_text.strip():
            skill_text = "general professional skills"

        # Import vector service for embedding
        from ..vector_services import vector_service
        return vector_service.generate_embedding(skill_text)

    def analyze_resume(self, file_path: str) -> Dict[str, Any]:
        """Complete resume analysis pipeline"""
        file_extension = Path(file_path).suffix.lower()

        # Extract text based on file type
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

        if not text:
            raise ValueError("Could not extract text from resume")

        # Analyze all components
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        education = self.extract_education(text)

        # Generate skill vector for AI matching
        skill_vector = self.generate_skill_vector(skills)

        # Calculate overall score (0-100)
        score = self.calculate_resume_score(skills, experience, education)

        return {
            "skills": skills,
            "experience": experience,
            "education": education,
            "skill_vector": skill_vector,
            "resume_score": score,
            "text_length": len(text),
            "analysis_timestamp": str(datetime.utcnow()),
            "ai_analysis": True
        }

    def calculate_resume_score(self, skills: Dict, experience: Dict, education: Dict) -> float:
        """Calculate overall resume score based on multiple factors"""
        score = 0

        # Skills score (40% weight)
        total_skills = sum(len(category) for category in skills.values())
        skill_score = min(total_skills * 5, 40)  # Max 40 points
        score += skill_score

        # Experience score (35% weight)
        exp_score = min(experience.get("years", 0) * 3.5, 35)  # Max 35 points
        score += exp_score

        # Education score (25% weight)
        education_weights = {"phd": 25, "masters": 20, "bachelors": 15, "diploma": 10}
        edu_score = education_weights.get(education.get("level", "diploma"), 10)
        score += edu_score

        return round(min(score, 100), 1)

    def get_job_matches(self, resume_analysis: Dict[str, Any], jobs_data: List[Dict]) -> List[Dict]:
        """Find best job matches based on resume analysis"""
        resume_vector = resume_analysis["skill_vector"]
        matches = []

        from ..vector_services import vector_service

        for job in jobs_data:
            if 'skill_vector' in job:
                try:
                    job_vector = json.loads(job['skill_vector'])
                    similarity = vector_service.cosine_similarity(resume_vector, job_vector)

                    # Calculate match score based on multiple factors
                    skill_match = similarity * 100
                    experience_match = self.calculate_experience_match(
                        resume_analysis["experience"],
                        job.get("experience_level", "mid")
                    )
                    education_match = self.calculate_education_match(
                        resume_analysis["education"]["level"],
                        job.get("required_education", "bachelors")
                    )

                    overall_score = (skill_match * 0.5) + (experience_match * 0.3) + (education_match * 0.2)

                    if overall_score > 30:  # Minimum threshold
                        matches.append({
                            **job,
                            "match_score": round(overall_score, 1),
                            "skill_similarity": round(skill_match, 1),
                            "experience_match": experience_match,
                            "education_match": education_match,
                            "match_reason": self.generate_match_reason(job, resume_analysis)
                        })
                except Exception as e:
                    print(f"⚠️ Error matching job {job.get('id')}: {e}")
                    continue

        return sorted(matches, key=lambda x: x["match_score"], reverse=True)[:10]

    def calculate_experience_match(self, candidate_exp: Dict, job_level: str) -> float:
        """Calculate experience match score"""
        level_mapping = {"entry": 1, "junior": 1, "mid": 2, "intermediate": 2, "senior": 3, "lead": 3}
        candidate_level = level_mapping.get(candidate_exp.get("level", "entry"), 1)
        job_required_level = level_mapping.get(job_level.lower(), 2)

        if candidate_level >= job_required_level:
            return 100
        elif candidate_level == job_required_level - 1:
            return 70
        else:
            return 30

    def calculate_education_match(self, candidate_edu: str, job_edu: str) -> float:
        """Calculate education match score"""
        education_hierarchy = ["diploma", "bachelors", "masters", "phd"]
        candidate_idx = education_hierarchy.index(candidate_edu) if candidate_edu in education_hierarchy else 1
        job_idx = education_hierarchy.index(job_edu) if job_edu in education_hierarchy else 1

        if candidate_idx >= job_idx:
            return 100
        elif candidate_idx == job_idx - 1:
            return 80
        else:
            return 40

    def generate_match_reason(self, job: Dict, resume: Dict) -> str:
        """Generate human-readable match explanation"""
        reasons = []

        # Skill-based reasons
        job_skills = job.get("skills", "").lower()
        resume_skills = " ".join(sum(resume["skills"].values(), [])).lower()

        matching_skills = []
        for skill in resume["skills"]["technical"] + resume["skills"]["domain"]:
            if skill.lower() in job_skills:
                matching_skills.append(skill)

        if matching_skills:
            reasons.append(f"Strong match in: {', '.join(matching_skills[:3])}")

        # Experience-based reasons
        exp_years = resume["experience"]["years"]
        if exp_years > 0:
            reasons.append(f"{exp_years} years of relevant experience")

        # Education-based reasons
        if resume["education"]["level"] != "diploma":
            reasons.append(f"{resume['education']['level'].title()} level education")

        return " • ".join(reasons) if reasons else "General skills alignment"

# Global instance
resume_parser = AdvancedResumeParser()