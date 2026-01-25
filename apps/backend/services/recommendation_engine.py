# services/recommendation_engine.py - Advanced AI Recommendation Engine
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Optional
import json
from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta

class AdvancedRecommendationEngine:
    def __init__(self):
        """Initialize the advanced recommendation engine"""
        self.scaler = StandardScaler()
        self.user_item_matrix = None
        self.item_similarity_matrix = None
        self.is_trained = False

        # Collaborative filtering parameters
        self.min_common_users = 3
        self.top_k_similar_items = 10

        print("✅ Advanced Recommendation Engine initialized!")

    def content_based_recommend(self, user_skills: List[str],
                              all_jobs: List[Dict], top_k: int = 5) -> List[Dict]:
        """Content-based filtering using skill vectors"""
        user_vector = self._get_user_skill_vector(user_skills)

        recommendations = []
        for job in all_jobs:
            if 'skill_vector' in job or 'desc_vector_json' in job:
                try:
                    # Try skill vector first, fallback to description vector
                    vector_field = 'skill_vector' if 'skill_vector' in job else 'desc_vector_json'
                    if vector_field.endswith('_json'):
                        job_vector = json.loads(job[vector_field])
                    else:
                        job_vector = job[vector_field]

                    similarity = self._calculate_similarity(user_vector, job_vector)

                    if similarity > 0.1:  # Minimum relevance threshold
                        recommendations.append({
                            **job,
                            'similarity_score': round(similarity * 100, 2),
                            'recommendation_type': 'content_based',
                            'match_confidence': self._calculate_confidence(similarity)
                        })
                except Exception as e:
                    print(f"⚠️ Error in content-based recommendation for job {job.get('id')}: {e}")
                    continue

        return sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)[:top_k]

    def collaborative_filter(self, user_history: List[Dict],
                           all_jobs: List[Dict], top_k: int = 5) -> List[Dict]:
        """Collaborative filtering based on user behavior patterns"""
        if not user_history:
            return []

        # Build user-item interaction matrix from history
        user_interactions = defaultdict(int)
        for interaction in user_history:
            job_id = interaction.get('job_id')
            interaction_type = interaction.get('type', 'view')
            weight = {'apply': 3, 'save': 2, 'view': 1}.get(interaction_type, 1)
            user_interactions[job_id] += weight

        # Find similar jobs based on user preferences
        recommendations = []
        interacted_job_ids = set(user_interactions.keys())

        for job in all_jobs:
            job_id = job.get('id') or job.get('job_id')
            if job_id in interacted_job_ids:
                continue  # Skip already interacted jobs

            # Calculate similarity to user's preferred jobs
            max_similarity = 0
            for interacted_id, weight in user_interactions.items():
                similar_job = next((j for j in all_jobs if (j.get('id') or j.get('job_id')) == interacted_id), None)
                if similar_job and 'skill_vector' in similar_job:
                    try:
                        sim_vector = similar_job.get('skill_vector')
                        job_vector = job.get('skill_vector')

                        if sim_vector and job_vector:
                            similarity = self._calculate_similarity(sim_vector, job_vector)
                            weighted_similarity = similarity * weight
                            max_similarity = max(max_similarity, weighted_similarity)
                    except:
                        continue

            if max_similarity > 0.15:  # Minimum collaborative threshold
                recommendations.append({
                    **job,
                    'collaborative_score': round(max_similarity * 100, 2),
                    'recommendation_type': 'collaborative',
                    'based_on_history': len(user_interactions)
                })

        return sorted(recommendations, key=lambda x: x['collaborative_score'], reverse=True)[:top_k]

    def hybrid_recommend(self, user_id: int, user_skills: List[str],
                        user_history: List[Dict], all_jobs: List[Dict],
                        weights: Dict[str, float] = None) -> List[Dict]:
        """Hybrid: Content-based + Collaborative filtering combined"""
        if weights is None:
            weights = {'content': 0.6, 'collaborative': 0.4}

        # Get recommendations from both methods
        content_recs = self.content_based_recommend(user_skills, all_jobs, 15)
        collaborative_recs = self.collaborative_filter(user_history, all_jobs, 15)

        # Combine and deduplicate
        all_recommendations = {}
        for rec in content_recs + collaborative_recs:
            job_id = rec.get('id') or rec.get('job_id')
            if job_id not in all_recommendations:
                all_recommendations[job_id] = rec.copy()
            else:
                # Merge scores if job appears in both lists
                existing = all_recommendations[job_id]
                content_score = rec.get('similarity_score', 0) * weights['content']
                collab_score = rec.get('collaborative_score', 0) * weights['collaborative']
                existing_score = existing.get('similarity_score', 0) * weights['content'] + \
                               existing.get('collaborative_score', 0) * weights['collaborative']

                combined_score = content_score + collab_score
                if combined_score > existing_score:
                    rec['hybrid_score'] = round(combined_score, 2)
                    rec['recommendation_type'] = 'hybrid'
                    all_recommendations[job_id] = rec

        # Sort by hybrid score and return top recommendations
        final_recs = list(all_recommendations.values())
        return sorted(final_recs, key=lambda x: x.get('hybrid_score', x.get('similarity_score', 0)),
                     reverse=True)[:10]

    def personalized_career_recommendations(self, user_profile: Dict[str, Any],
                                          all_careers: List[Dict], top_k: int = 5) -> List[Dict]:
        """Personalized career recommendations based on user profile"""
        user_vector = self._build_user_profile_vector(user_profile)

        recommendations = []
        for career in all_careers:
            if 'skills_vector_json' in career:
                try:
                    career_vector = json.loads(career['skills_vector_json'])
                    similarity = self._calculate_similarity(user_vector, career_vector)

                    # Calculate career fit based on multiple factors
                    skill_fit = similarity * 100
                    experience_fit = self._calculate_experience_career_fit(
                        user_profile.get('experience_years', 0),
                        career.get('experience_level', 'mid')
                    )
                    growth_potential = career.get('demand', 50) / 100 * 100  # Normalize demand score

                    overall_fit = (skill_fit * 0.4) + (experience_fit * 0.4) + (growth_potential * 0.2)

                    if overall_fit > 40:  # Minimum career fit threshold
                        recommendations.append({
                            **career,
                            'career_fit_score': round(overall_fit, 1),
                            'skill_alignment': round(skill_fit, 1),
                            'experience_fit': round(experience_fit, 1),
                            'growth_potential': round(growth_potential, 1),
                            'recommendation_type': 'career_guidance',
                            'reasoning': self._generate_career_reasoning(career, user_profile)
                        })
                except Exception as e:
                    print(f"⚠️ Error in career recommendation for {career.get('title')}: {e}")
                    continue

        return sorted(recommendations, key=lambda x: x['career_fit_score'], reverse=True)[:top_k]

    def skill_gap_analysis(self, current_skills: List[str], target_role: str,
                          all_careers: List[Dict]) -> Dict[str, Any]:
        """Analyze skill gaps for career progression"""
        # Find target career requirements
        target_career = None
        for career in all_careers:
            if career.get('title', '').lower().replace(' ', '') == target_role.lower().replace(' ', ''):
                target_career = career
                break

        if not target_career:
            return {"error": f"Career '{target_role}' not found"}

        # Extract required skills from career description
        required_skills = self._extract_career_skills(target_career)
        current_skill_set = set(skill.lower() for skill in current_skills)
        required_skill_set = set(skill.lower() for skill in required_skills)

        missing_skills = required_skill_set - current_skill_set
        matching_skills = current_skill_set.intersection(required_skill_set)

        # Calculate gap metrics
        total_required = len(required_skill_set)
        skills_matched = len(matching_skills)
        skills_missing = len(missing_skills)
        gap_percentage = (skills_missing / total_required * 100) if total_required > 0 else 0

        return {
            "target_career": target_role,
            "required_skills": list(required_skill_set),
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "gap_analysis": {
                "total_required": total_required,
                "skills_matched": skills_matched,
                "skills_missing": skills_missing,
                "gap_percentage": round(gap_percentage, 1),
                "readiness_level": self._calculate_readiness_level(gap_percentage)
            },
            "learning_recommendations": self._generate_learning_path(list(missing_skills))
        }

    def _get_user_skill_vector(self, skills: List[str]) -> List[float]:
        """Generate vector representation of user skills"""
        from ..vector_services import vector_service
        skill_text = " ".join(skills) if skills else "general professional skills"
        return vector_service.generate_embedding(skill_text)

    def _calculate_similarity(self, vec1, vec2) -> float:
        """Calculate cosine similarity between vectors"""
        from ..vector_services import vector_service
        return vector_service.cosine_similarity(vec1, vec2)

    def _calculate_confidence(self, similarity: float) -> str:
        """Convert similarity score to confidence level"""
        if similarity >= 0.8:
            return "Very High"
        elif similarity >= 0.6:
            return "High"
        elif similarity >= 0.4:
            return "Medium"
        elif similarity >= 0.2:
            return "Low"
        else:
            return "Very Low"

    def _build_user_profile_vector(self, user_profile: Dict[str, Any]) -> List[float]:
        """Build comprehensive user profile vector"""
        profile_components = []

        # Skills component
        skills = user_profile.get('skills', [])
        if skills:
            profile_components.append(" ".join(skills))

        # Experience component
        experience_years = user_profile.get('experience_years', 0)
        profile_components.append(f"experience {experience_years} years")

        # Education component
        education = user_profile.get('education', 'bachelors')
        profile_components.append(f"education {education}")

        # Interests component
        interests = user_profile.get('interests', [])
        if interests:
            profile_components.append(" ".join(interests))

        profile_text = " ".join(profile_components)
        if not profile_text.strip():
            profile_text = "general professional background"

        from ..vector_services import vector_service
        return vector_service.generate_embedding(profile_text)

    def _calculate_experience_career_fit(self, user_years: int, career_level: str) -> float:
        """Calculate how well user's experience fits career requirements"""
        level_requirements = {
            "entry": (0, 2),
            "junior": (1, 3),
            "mid": (2, 5),
            "intermediate": (3, 7),
            "senior": (5, 10),
            "lead": (7, 15),
            "executive": (10, 20)
        }

        min_years, max_years = level_requirements.get(career_level.lower(), (2, 5))

        if user_years >= min_years and user_years <= max_years:
            return 100
        elif user_years > max_years:
            # Too experienced but still qualified
            return max(70, 100 - (user_years - max_years) * 5)
        else:
            # Less experience than required
            return max(30, (user_years / min_years) * 80)

    def _extract_career_skills(self, career: Dict[str, Any]) -> List[str]:
        """Extract required skills from career data"""
        skills = []

        # From description
        description = career.get('description', '')
        if description:
            # Simple keyword extraction (could be enhanced with NLP)
            skill_keywords = [
                'python', 'java', 'javascript', 'data analysis', 'machine learning',
                'project management', 'communication', 'leadership', 'agile', 'scrum',
                'renewable energy', 'sustainability', 'solar', 'wind', 'engineering'
            ]

            for keyword in skill_keywords:
                if keyword in description.lower():
                    skills.append(keyword.title())

        # From required_skills field if available
        required_skills = career.get('required_skills', [])
        if isinstance(required_skills, list):
            skills.extend(required_skills)
        elif isinstance(required_skills, str):
            try:
                parsed_skills = json.loads(required_skills)
                if isinstance(parsed_skills, list):
                    skills.extend(parsed_skills)
            except:
                skills.append(required_skills)

        return list(set(skills))  # Remove duplicates

    def _calculate_readiness_level(self, gap_percentage: float) -> str:
        """Convert gap percentage to readiness level"""
        if gap_percentage <= 20:
            return "Ready"
        elif gap_percentage <= 40:
            return "Mostly Ready"
        elif gap_percentage <= 60:
            return "Needs Some Training"
        elif gap_percentage <= 80:
            return "Significant Skill Gap"
        else:
            return "Major Retraining Required"

    def _generate_learning_path(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generate learning recommendations for missing skills"""
        learning_resources = {
            "python": {
                "platform": "Coursera",
                "course": "Python for Everybody",
                "duration": "8 weeks",
                "level": "Beginner",
                "cost": "Free"
            },
            "machine learning": {
                "platform": "edX",
                "course": "Machine Learning with Python",
                "duration": "12 weeks",
                "level": "Intermediate",
                "cost": "Free"
            },
            "data analysis": {
                "platform": "DataCamp",
                "course": "Data Analyst with Python",
                "duration": "4 months",
                "level": "Beginner to Intermediate",
                "cost": "$25/month"
            },
            "project management": {
                "platform": "Coursera",
                "course": "Google Project Management",
                "duration": "6 months",
                "level": "Beginner",
                "cost": "Free"
            }
        }

        recommendations = []
        for skill in missing_skills[:5]:  # Limit to top 5 skills
            skill_lower = skill.lower()
            if skill_lower in learning_resources:
                resource = learning_resources[skill_lower]
                recommendations.append({
                    "skill": skill,
                    **resource
                })
            else:
                # Generic recommendation
                recommendations.append({
                    "skill": skill,
                    "platform": "YouTube/Google",
                    "course": f"{skill} Fundamentals",
                    "duration": "4-6 weeks",
                    "level": "Self-paced",
                    "cost": "Free"
                })

        return recommendations

    def _generate_career_reasoning(self, career: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        """Generate human-readable reasoning for career recommendation"""
        reasons = []

        # Growth potential
        demand = career.get('demand', 50)
        if demand >= 90:
            reasons.append("High demand career with excellent growth prospects")

        # Salary potential
        salary_range = career.get('salary_range', '')
        if '15' in salary_range or '20' in salary_range or '25' in salary_range:
            reasons.append("Strong salary potential")

        # Experience fit
        exp_years = user_profile.get('experience_years', 0)
        career_level = career.get('experience_level', 'mid')
        if exp_years >= 3 and 'mid' in career_level.lower():
            reasons.append("Good experience fit for your background")

        return " • ".join(reasons) if reasons else "Good overall career match"

# Global instance
recommendation_engine = AdvancedRecommendationEngine()