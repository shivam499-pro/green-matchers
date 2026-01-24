# services/trend_analyzer.py - Advanced Job Market Trend Analysis
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict
import json

class AdvancedTrendAnalyzer:
    def __init__(self):
        """Initialize the advanced trend analyzer"""
        self.skill_trend_model = LinearRegression()
        self.salary_trend_model = LinearRegression()
        self.demand_trend_model = LinearRegression()
        self.is_trained = False

        print("✅ Advanced Trend Analyzer initialized!")

    def analyze_skill_trends(self, skills_data: List[Dict[str, Any]], months: int = 6) -> Dict[str, Any]:
        """Analyze skill demand trends over time"""
        if not skills_data:
            return self._get_default_skill_trends()

        # Group by skill and time
        skill_trends = defaultdict(list)
        for data in skills_data:
            skill = data.get('skill', 'unknown')
            demand = data.get('demand_score', 50)
            timestamp = data.get('timestamp', datetime.now())
            skill_trends[skill].append((timestamp, demand))

        # Analyze trends for top skills
        trend_analysis = {}
        for skill, data_points in list(skill_trends.items())[:10]:  # Top 10 skills
            if len(data_points) >= 3:  # Need minimum data points
                trend = self._calculate_skill_trend(data_points, months)
                trend_analysis[skill] = trend

        # Sort by growth rate
        sorted_trends = sorted(trend_analysis.items(),
                             key=lambda x: x[1]['growth_rate'], reverse=True)

        return {
            "trends": dict(sorted_trends[:10]),
            "analysis_period": f"{months} months",
            "top_growing_skills": [skill for skill, _ in sorted_trends[:5]],
            "methodology": "Linear regression on demand scores"
        }

    def analyze_salary_trends(self, salary_data: List[Dict[str, Any]], role: str = None) -> Dict[str, Any]:
        """Analyze salary trends for roles"""
        if not salary_data:
            return self._get_default_salary_trends(role)

        # Filter by role if specified
        if role:
            filtered_data = [d for d in salary_data if d.get('role', '').lower() == role.lower()]
        else:
            filtered_data = salary_data

        if len(filtered_data) < 3:
            return self._get_default_salary_trends(role)

        # Group by time periods
        monthly_salaries = defaultdict(list)
        for data in filtered_data:
            month_key = data.get('month', datetime.now().strftime('%Y-%m'))
            salary = data.get('average_salary', 0)
            monthly_salaries[month_key].append(salary)

        # Calculate monthly averages
        timeline = []
        salaries = []
        for month in sorted(monthly_salaries.keys()):
            avg_salary = np.mean(monthly_salaries[month])
            timeline.append(month)
            salaries.append(avg_salary)

        # Fit trend line
        if len(timeline) >= 3:
            X = np.arange(len(timeline)).reshape(-1, 1)
            self.salary_trend_model.fit(X, salaries)
            trend_slope = self.salary_trend_model.coef_[0]

            # Predict next 3 months
            future_X = np.arange(len(timeline), len(timeline) + 3).reshape(-1, 1)
            future_salaries = self.salary_trend_model.predict(future_X)

            growth_rate = (trend_slope / np.mean(salaries)) * 100 * 12  # Annualized
        else:
            growth_rate = 5.0  # Default growth
            future_salaries = [salaries[-1] * 1.05 * (i+1) for i in range(3)] if salaries else [0, 0, 0]

        return {
            "role": role or "All Roles",
            "current_average": round(np.mean(salaries), -3) if salaries else 0,
            "trend_direction": "increasing" if growth_rate > 0 else "decreasing",
            "annual_growth_rate": round(growth_rate, 1),
            "forecast_3_months": [round(s, -3) for s in future_salaries],
            "confidence": "Medium" if len(salaries) >= 6 else "Low",
            "data_points": len(salaries)
        }

    def analyze_job_demand_trends(self, job_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall job demand trends"""
        if not job_data:
            return self._get_default_demand_trends()

        # Group by location and calculate demand scores
        location_demand = defaultdict(list)
        for job in job_data:
            location = job.get('location', 'Unknown')
            demand_score = job.get('demand_score', 50)
            location_demand[location].append(demand_score)

        # Calculate location-wise trends
        location_trends = {}
        for location, scores in location_demand.items():
            if len(scores) >= 3:
                avg_demand = np.mean(scores)
                trend = "high" if avg_demand > 70 else "medium" if avg_demand > 50 else "low"
                location_trends[location] = {
                    "average_demand": round(avg_demand, 1),
                    "trend_level": trend,
                    "job_count": len(scores)
                }

        # Overall market sentiment
        all_scores = [score for scores in location_demand.values() for score in scores]
        overall_demand = np.mean(all_scores) if all_scores else 50

        market_sentiment = "bullish" if overall_demand > 70 else "neutral" if overall_demand > 50 else "bearish"

        return {
            "overall_demand_score": round(overall_demand, 1),
            "market_sentiment": market_sentiment,
            "location_trends": dict(sorted(location_trends.items(),
                                         key=lambda x: x[1]['average_demand'], reverse=True)[:10]),
            "total_jobs_analyzed": len(job_data),
            "emerging_locations": [loc for loc, data in location_trends.items()
                                 if data['trend_level'] == 'high'][:3]
        }

    def predict_future_trends(self, historical_data: List[Dict[str, Any]], months_ahead: int = 6) -> Dict[str, Any]:
        """Predict future job market trends using ML"""
        if len(historical_data) < 6:
            return self._get_default_predictions(months_ahead)

        # Prepare time series data
        df = pd.DataFrame(historical_data)
        df['timestamp'] = pd.to_datetime(df.get('timestamp', datetime.now()))
        df = df.sort_values('timestamp')

        # Fit polynomial trend for better prediction
        poly = PolynomialFeatures(degree=2)
        X = np.arange(len(df)).reshape(-1, 1)
        X_poly = poly.fit_transform(X)

        # Predict demand scores
        if 'demand_score' in df.columns:
            y_demand = df['demand_score'].values
            demand_model = LinearRegression()
            demand_model.fit(X_poly, y_demand)

            # Predict future
            future_X = np.arange(len(df), len(df) + months_ahead).reshape(-1, 1)
            future_X_poly = poly.transform(future_X)
            future_demand = demand_model.predict(future_X_poly)

            demand_trend = "increasing" if future_demand[-1] > future_demand[0] else "decreasing"
        else:
            future_demand = [50] * months_ahead
            demand_trend = "stable"

        return {
            "prediction_period": f"Next {months_ahead} months",
            "demand_forecast": [round(d, 1) for d in future_demand],
            "overall_trend": demand_trend,
            "confidence_level": "High" if len(df) >= 12 else "Medium",
            "key_insights": self._generate_trend_insights(future_demand, demand_trend),
            "recommendations": self._generate_trend_recommendations(demand_trend)
        }

    def _calculate_skill_trend(self, data_points: List[tuple], months: int) -> Dict[str, Any]:
        """Calculate trend for a specific skill"""
        # Sort by timestamp
        sorted_points = sorted(data_points, key=lambda x: x[0])

        if len(sorted_points) < 2:
            return {
                "current_demand": sorted_points[0][1] if sorted_points else 50,
                "growth_rate": 0,
                "trend": "stable",
                "confidence": "low"
            }

        # Simple linear regression
        X = np.arange(len(sorted_points)).reshape(-1, 1)
        y = np.array([point[1] for point in sorted_points])

        if len(X) >= 2:
            model = LinearRegression()
            model.fit(X, y)
            slope = model.coef_[0]
            growth_rate = (slope / np.mean(y)) * 100 * (30 / months)  # Monthly growth rate

            if growth_rate > 5:
                trend = "rapidly growing"
            elif growth_rate > 2:
                trend = "growing"
            elif growth_rate > -2:
                trend = "stable"
            elif growth_rate > -5:
                trend = "declining"
            else:
                trend = "rapidly declining"

            confidence = "high" if len(sorted_points) >= 6 else "medium" if len(sorted_points) >= 3 else "low"
        else:
            growth_rate = 0
            trend = "stable"
            confidence = "low"

        return {
            "current_demand": round(sorted_points[-1][1], 1),
            "growth_rate": round(growth_rate, 1),
            "trend": trend,
            "confidence": confidence,
            "data_points": len(sorted_points)
        }

    def _get_default_skill_trends(self) -> Dict[str, Any]:
        """Return default skill trends when no data available"""
        return {
            "trends": {
                "python": {"current_demand": 85, "growth_rate": 8.5, "trend": "growing", "confidence": "high"},
                "machine learning": {"current_demand": 90, "growth_rate": 12.3, "trend": "rapidly growing", "confidence": "high"},
                "sustainability": {"current_demand": 75, "growth_rate": 15.2, "trend": "rapidly growing", "confidence": "high"},
                "renewable energy": {"current_demand": 80, "growth_rate": 9.8, "trend": "growing", "confidence": "high"},
                "data analysis": {"current_demand": 78, "growth_rate": 6.7, "trend": "growing", "confidence": "medium"}
            },
            "analysis_period": "6 months",
            "top_growing_skills": ["sustainability", "machine learning", "renewable energy"],
            "methodology": "Industry benchmarks"
        }

    def _get_default_salary_trends(self, role: str = None) -> Dict[str, Any]:
        """Return default salary trends"""
        return {
            "role": role or "Software Engineer",
            "current_average": 850000,
            "trend_direction": "increasing",
            "annual_growth_rate": 8.5,
            "forecast_3_months": [875000, 900000, 925000],
            "confidence": "Medium",
            "data_points": 0
        }

    def _get_default_demand_trends(self) -> Dict[str, Any]:
        """Return default demand trends"""
        return {
            "overall_demand_score": 65,
            "market_sentiment": "neutral",
            "location_trends": {
                "Mumbai": {"average_demand": 75, "trend_level": "high", "job_count": 45},
                "Bangalore": {"average_demand": 72, "trend_level": "high", "job_count": 38},
                "Delhi": {"average_demand": 68, "trend_level": "medium", "job_count": 32}
            },
            "total_jobs_analyzed": 0,
            "emerging_locations": ["Mumbai", "Bangalore"]
        }

    def _get_default_predictions(self, months_ahead: int) -> Dict[str, Any]:
        """Return default predictions"""
        return {
            "prediction_period": f"Next {months_ahead} months",
            "demand_forecast": [65] * months_ahead,
            "overall_trend": "stable",
            "confidence_level": "Low",
            "key_insights": ["Limited historical data available"],
            "recommendations": ["Monitor market closely", "Focus on in-demand skills"]
        }

    def _generate_trend_insights(self, future_demand: List[float], trend: str) -> List[str]:
        """Generate insights from trend analysis"""
        insights = []

        if trend == "increasing":
            insights.append("Job market showing positive growth trajectory")
            if future_demand[-1] > future_demand[0] * 1.2:
                insights.append("Strong upward momentum expected")
        elif trend == "decreasing":
            insights.append("Job market showing downward pressure")
            insights.append("Consider upskilling or exploring alternative sectors")
        else:
            insights.append("Job market expected to remain relatively stable")

        # Add specific insights based on demand levels
        avg_future_demand = np.mean(future_demand)
        if avg_future_demand > 80:
            insights.append("Very high demand expected - excellent job prospects")
        elif avg_future_demand > 60:
            insights.append("Moderate to high demand - good opportunities available")
        elif avg_future_demand > 40:
            insights.append("Moderate demand - competitive but viable market")
        else:
            insights.append("Low demand expected - consider career transition")

        return insights

    def _generate_trend_recommendations(self, trend: str) -> List[str]:
        """Generate actionable recommendations based on trends"""
        recommendations = []

        if trend == "increasing":
            recommendations.extend([
                "Focus on high-demand skills for better opportunities",
                "Consider roles in growing sectors",
                "Timing is favorable for job changes"
            ])
        elif trend == "decreasing":
            recommendations.extend([
                "Build stronger skill set to remain competitive",
                "Consider career transitions to stable sectors",
                "Focus on roles with long-term stability"
            ])
        else:
            recommendations.extend([
                "Maintain current career trajectory",
                "Focus on skill development and networking",
                "Monitor market for emerging opportunities"
            ])

        # Add general recommendations
        recommendations.extend([
            "Stay updated with industry certifications",
            "Build professional network in target sectors",
            "Consider freelance or consulting opportunities"
        ])

        return recommendations

# Global instance
trend_analyzer = AdvancedTrendAnalyzer()