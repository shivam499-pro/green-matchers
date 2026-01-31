# services/job_enhancer.py - AI-Powered Job Description Enhancement
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class AdvancedJobEnhancer:
    def __init__(self):
        """Initialize the advanced job description enhancer"""
        try:
            # Use T5 model for text enhancement (smaller and more practical than GPT)
            model_name = "t5-small"  # More practical than large models
            self.enhancer_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.enhancer_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

            # Note: BART compression moved to dedicated BARTCompressionEngine service

            self.is_initialized = True
            print("✅ Advanced Job Enhancer initialized with T5 model!")
        except Exception as e:
            print(f"⚠️ Job enhancer initialization failed: {e}")
            print("🔄 Falling back to rule-based enhancement")
            self.is_initialized = False

        # Predefined enhancement templates
        self.enhancement_templates = {
            "responsibilities": [
                "Develop and maintain {skill} solutions",
                "Collaborate with cross-functional teams",
                "Ensure compliance with industry standards",
                "Drive innovation in {domain} technologies",
                "Mentor junior team members",
                "Participate in code reviews and quality assurance"
            ],
            "requirements": [
                "Bachelor's degree in relevant field",
                "Strong proficiency in {skill}",
                "Experience with {domain} projects",
                "Excellent problem-solving abilities",
                "Strong communication and teamwork skills",
                "Knowledge of industry best practices"
            ],
            "benefits": [
                "Competitive salary package",
                "Health and wellness programs",
                "Professional development opportunities",
                "Flexible work arrangements",
                "Collaborative work environment",
                "Performance-based incentives"
            ]
        }

    def enhance_job_description(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance a complete job description with AI"""
        enhanced_job = job_data.copy()

        # Extract original components
        title = job_data.get('title', '')
        description = job_data.get('description', '')
        requirements = job_data.get('requirements', '')
        company = job_data.get('company', '')

        # Enhance title if too basic
        enhanced_job['enhanced_title'] = self._enhance_job_title(title, description)

        # Enhance description
        enhanced_job['enhanced_description'] = self._enhance_description(description, title)

        # Generate comprehensive requirements
        enhanced_job['enhanced_requirements'] = self._enhance_requirements(requirements, title, description)

        # Generate benefits section
        enhanced_job['benefits'] = self._generate_benefits_section(company, title)

        # Generate company culture section
        enhanced_job['company_culture'] = self._generate_company_culture(company)

        # Calculate enhancement score
        enhanced_job['enhancement_score'] = self._calculate_enhancement_score(job_data, enhanced_job)

        return enhanced_job

    def _enhance_job_title(self, title: str, description: str) -> str:
        """Enhance job title to be more attractive and specific"""
        if not title:
            return "Professional Position"

        # Make titles more specific and attractive
        title_enhancements = {
            "developer": "Senior Software Developer",
            "engineer": "Senior Software Engineer",
            "analyst": "Senior Data Analyst",
            "manager": "Senior Project Manager",
            "specialist": "Technical Specialist",
            "consultant": "Senior Technology Consultant"
        }

        lower_title = title.lower()
        for key, enhanced in title_enhancements.items():
            if key in lower_title and len(title.split()) <= 2:
                return enhanced

        # If title is already detailed, return as-is
        if len(title.split()) >= 3:
            return title

        # Try to infer from description keywords
        if description:
            desc_lower = description.lower()
            if "machine learning" in desc_lower or "ai" in desc_lower:
                return f"AI/ML {title}"
            elif "data" in desc_lower:
                return f"Data {title}"
            elif "sustainability" in desc_lower or "green" in desc_lower:
                return f"Green Energy {title}"

        return title

    def _enhance_description(self, description: str, title: str) -> str:
        """Enhance job description with AI or rule-based approach"""
        if not description:
            return self._generate_description_from_title(title)

        # If AI models are available, use them
        if self.is_initialized:
            try:
                return self._ai_enhance_description(description)
            except Exception as e:
                print(f"⚠️ AI enhancement failed, using rule-based: {e}")

        # Fallback to rule-based enhancement
        return self._rule_based_enhance_description(description, title)

    def _ai_enhance_description(self, description: str) -> str:
        """Use AI models to enhance description"""
        # Use T5 for text enhancement
        input_text = f"enhance job description: {description[:512]}"  # Limit input length

        inputs = self.enhancer_tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.enhancer_model.generate(
            inputs.input_ids,
            max_length=300,
            num_beams=4,
            early_stopping=True
        )

        enhanced = self.enhancer_tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean up the output
        enhanced = self._clean_enhanced_text(enhanced)

        return enhanced if len(enhanced) > len(description) * 0.8 else description

    def _rule_based_enhance_description(self, description: str, title: str) -> str:
        """Rule-based description enhancement"""
        enhanced_parts = []

        # Add compelling introduction
        intro_templates = [
            f"Join our dynamic team as a {title} and contribute to innovative projects that make a difference.",
            f"We're seeking a talented {title} to drive impactful solutions in our growing organization.",
            f"Exciting opportunity for a skilled {title} to work on cutting-edge technologies and projects."
        ]

        enhanced_parts.append(intro_templates[len(description) % len(intro_templates)])

        # Add original description
        enhanced_parts.append(description)

        # Add motivational closing
        closing_templates = [
            "This role offers significant growth opportunities and the chance to work with cutting-edge technologies.",
            "You'll be part of a collaborative team dedicated to delivering exceptional results.",
            "We offer competitive compensation and a supportive work environment for professional development."
        ]

        enhanced_parts.append(closing_templates[len(description) % len(closing_templates)])

        return "\n\n".join(enhanced_parts)

    def _enhance_requirements(self, requirements: str, title: str, description: str) -> str:
        """Enhance requirements section"""
        if not requirements:
            return self._generate_requirements_from_title(title, description)

        # Extract skills from title and description
        extracted_skills = self._extract_skills_from_text(title + " " + description)

        # Combine existing requirements with enhanced ones
        enhanced_reqs = []

        # Add existing requirements
        if requirements:
            enhanced_reqs.append("Current Requirements:")
            enhanced_reqs.append(requirements)

        # Add enhanced requirements based on extracted skills
        if extracted_skills:
            enhanced_reqs.append("\nKey Technical Skills:")
            for skill in extracted_skills[:5]:  # Top 5 skills
                enhanced_reqs.append(f"• Proficiency in {skill}")

        # Add standard professional requirements
        enhanced_reqs.append("\nProfessional Qualifications:")
        enhanced_reqs.extend([
            "• Bachelor's degree in relevant field or equivalent experience",
            "• Strong analytical and problem-solving abilities",
            "• Excellent communication and interpersonal skills",
            "• Ability to work effectively in collaborative environments",
            "• Commitment to continuous learning and professional development"
        ])

        return "\n".join(enhanced_reqs)

    def _generate_description_from_title(self, title: str) -> str:
        """Generate description when none exists"""
        title_lower = title.lower()

        if "developer" in title_lower or "engineer" in title_lower:
            return """We are seeking a skilled developer/engineer to join our innovative team.

            In this role, you will be responsible for designing, developing, and maintaining high-quality software solutions. You will collaborate with cross-functional teams to deliver projects that meet business objectives and technical requirements.

            This position offers an opportunity to work with cutting-edge technologies and contribute to meaningful projects that impact our organization and community."""

        elif "analyst" in title_lower:
            return """Join our analytics team as a data analyst where you'll transform data into actionable insights.

            You will work with large datasets, perform complex analyses, and create visualizations to support data-driven decision making. Your work will directly influence business strategy and operational improvements.

            We offer a collaborative environment with opportunities for professional growth and development."""

        else:
            return f"""We are looking for a talented {title} to join our growing team.

            In this dynamic role, you will contribute your expertise to drive innovation and achieve organizational goals. You will work closely with colleagues to deliver high-quality results and support our mission.

            This position offers competitive compensation, professional development opportunities, and a supportive work environment."""

    def _generate_requirements_from_title(self, title: str, description: str) -> str:
        """Generate requirements when none exist"""
        skills = self._extract_skills_from_text(title + " " + description)

        requirements = ["Required Qualifications:"]

        if skills:
            requirements.append("Technical Skills:")
            for skill in skills:
                requirements.append(f"• {skill}")
        else:
            requirements.extend([
                "• Bachelor's degree in relevant field",
                "• 2+ years of related experience",
                "• Strong technical skills"
            ])

        requirements.extend([
            "",
            "Preferred Qualifications:",
            "• Advanced degree in relevant field",
            "• Professional certifications",
            "• Experience with industry-standard tools",
            "",
            "Soft Skills:",
            "• Excellent communication abilities",
            "• Strong problem-solving skills",
            "• Ability to work in team environments"
        ])

        return "\n".join(requirements)

    def _generate_benefits_section(self, company: str, title: str) -> str:
        """Generate comprehensive benefits section"""
        benefits = [f"What We Offer at {company or 'Our Company'}:"]
        benefits.extend([
            "",
            "Compensation & Rewards:",
            "• Competitive salary package",
            "• Performance-based incentives",
            "• Annual bonus opportunities",
            "",
            "Health & Wellness:",
            "• Comprehensive health insurance",
            "• Dental and vision coverage",
            "• Mental health support programs",
            "",
            "Professional Development:",
            "• Training and certification opportunities",
            "• Conference attendance support",
            "• Career advancement programs",
            "",
            "Work-Life Balance:",
            "• Flexible work arrangements",
            "• Generous paid time off",
            "• Remote work options",
            "",
            "Additional Perks:",
            "• Modern office facilities",
            "• Team building activities",
            "• Employee assistance programs"
        ])

        return "\n".join(benefits)

    def _generate_company_culture(self, company: str) -> str:
        """Generate company culture section"""
        culture_templates = [
            f"At {company or 'our organization'}, we foster a culture of innovation, collaboration, and continuous learning. Our team is passionate about making a positive impact while maintaining work-life balance and supporting professional growth.",
            f"Join {company or 'our company'} where innovation meets purpose. We believe in empowering our employees to do their best work while creating solutions that benefit society and the environment.",
            f"Our culture at {company or 'the company'} emphasizes teamwork, creativity, and social responsibility. We provide the resources and support needed for our employees to thrive and make meaningful contributions."
        ]

        return culture_templates[len((company or "")) % len(culture_templates)]

    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract relevant skills from text"""
        skill_keywords = {
            "python": ["python", "django", "flask", "pandas", "numpy"],
            "javascript": ["javascript", "react", "node.js", "angular", "vue"],
            "data_science": ["machine learning", "data analysis", "statistics", "sql", "r"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes"],
            "soft_skills": ["communication", "leadership", "problem solving", "teamwork"]
        }

        found_skills = []
        text_lower = text.lower()

        for category, keywords in skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if category == "python":
                        found_skills.append("Python programming")
                    elif category == "javascript":
                        found_skills.append("JavaScript/TypeScript")
                    elif category == "data_science":
                        found_skills.append("Data Science & Analytics")
                    elif category == "cloud":
                        found_skills.append("Cloud Technologies")
                    elif category == "soft_skills":
                        found_skills.append(keyword.title())
                    break

        return list(set(found_skills))  # Remove duplicates

    def _clean_enhanced_text(self, text: str) -> str:
        """Clean up AI-generated text"""
        # Remove extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'\s+', ' ', text)

        # Capitalize first letter of sentences
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        cleaned_sentences = []

        for sentence in sentences:
            if sentence:
                cleaned_sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                cleaned_sentences.append(cleaned_sentence)

        return ' '.join(cleaned_sentences)

    def _calculate_enhancement_score(self, original: Dict[str, Any], enhanced: Dict[str, Any]) -> float:
        """Calculate how much the job description was enhanced"""
        original_length = len((original.get('description', '') + original.get('requirements', '')))
        enhanced_length = len((enhanced.get('enhanced_description', '') + enhanced.get('enhanced_requirements', '')))

        # Calculate improvement metrics
        length_improvement = (enhanced_length - original_length) / max(original_length, 1)
        features_added = sum(1 for key in ['benefits', 'company_culture', 'enhanced_title']
                           if key in enhanced and enhanced[key])

        # Combine metrics
        score = min(100, (length_improvement * 30) + (features_added * 20) + 50)

        return round(score, 1)

# Global instance
job_enhancer = AdvancedJobEnhancer()