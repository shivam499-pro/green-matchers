# services/salary_predictor.py - Advanced ML Salary Prediction
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import json
from datetime import datetime

class AdvancedSalaryPredictor:
    def __init__(self):
        """Initialize the advanced salary prediction model"""
        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'experience_years', 'skill_count', 'location_encoded',
            'company_size_encoded', 'education_encoded', 'role_seniority_encoded'
        ]
        self.is_trained = False
        self.training_accuracy = 0.0

        print("✅ Advanced Salary Predictor initialized!")

    def train_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train the salary prediction model with comprehensive data"""
        if len(training_data) < 10:
            return {"status": "insufficient_data", "message": "Need at least 10 data points"}

        # Convert to DataFrame
        df = pd.DataFrame(training_data)

        # Handle missing values
        df = df.fillna({
            'experience_years': df['experience_years'].median(),
            'skill_count': df['skill_count'].median(),
            'company_size': 'Medium',
            'education': 'bachelors',
            'role_seniority': 'mid'
        })

        # Encode categorical variables
        categorical_cols = ['location', 'company_size', 'education', 'role_seniority']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col].astype(str))

        # Prepare features and target
        X = df[self.feature_columns]
        y = df['salary']

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate model
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        self.training_accuracy = r2

        return {
            "status": "trained",
            "accuracy": round(r2 * 100, 2),
            "mae": round(mae, 2),
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }

    def predict_salary(self, job_features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict salary with confidence intervals"""
        if not self.is_trained:
            # Fallback prediction based on experience and skills
            return self._fallback_prediction(job_features)

        try:
            # Prepare features
            features = self._prepare_features(job_features)
            features_scaled = self.scaler.transform([features])

            # Get prediction and uncertainty
            prediction = self.model.predict(features_scaled)[0]

            # Calculate confidence interval using prediction variance
            # For Random Forest, we can use the variance of tree predictions
            tree_predictions = np.array([tree.predict(features_scaled) for tree in self.model.estimators_])
            std_dev = np.std(tree_predictions)

            confidence_interval = {
                "lower": max(0, prediction - 1.96 * std_dev),
                "upper": prediction + 1.96 * std_dev
            }

            # Determine confidence level
            confidence_level = self._calculate_confidence_level(std_dev / prediction)

            return {
                "predicted_salary": round(prediction, -2),  # Round to nearest 100
                "confidence_interval": {
                    "lower": round(confidence_interval["lower"], -2),
                    "upper": round(confidence_interval["upper"], -2)
                },
                "confidence_level": confidence_level,
                "currency": "INR",
                "model_accuracy": round(self.training_accuracy * 100, 1),
                "factors_influencing": self._explain_prediction(job_features),
                "market_comparison": self._compare_to_market(prediction, job_features)
            }

        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return self._fallback_prediction(job_features)

    def predict_salary_range(self, job_features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict salary range with detailed breakdown"""
        base_prediction = self.predict_salary(job_features)

        # Add location-based adjustments
        location_multiplier = self._get_location_multiplier(job_features.get('location', ''))
        adjusted_prediction = base_prediction["predicted_salary"] * location_multiplier

        # Add experience-based adjustments
        experience_bonus = self._calculate_experience_bonus(job_features.get('experience_years', 0))
        final_prediction = adjusted_prediction * (1 + experience_bonus)

        return {
            **base_prediction,
            "base_salary": base_prediction["predicted_salary"],
            "location_adjusted": round(adjusted_prediction, -2),
            "experience_adjusted": round(final_prediction, -2),
            "adjustments": {
                "location_factor": round(location_multiplier, 2),
                "experience_bonus": round(experience_bonus, 2)
            }
        }

    def forecast_salary_trends(self, role: str, years_ahead: int = 3) -> Dict[str, Any]:
        """Forecast salary trends for a role"""
        # This would typically use time series analysis
        # For now, provide rule-based forecasting

        base_forecasts = {
            "data scientist": [950000, 1050000, 1150000],
            "software engineer": [850000, 950000, 1050000],
            "renewable energy engineer": [750000, 850000, 950000],
            "sustainability manager": [900000, 1000000, 1100000],
            "default": [700000, 800000, 900000]
        }

        forecasts = base_forecasts.get(role.lower(), base_forecasts["default"])

        return {
            "role": role,
            "forecast_period": f"Next {years_ahead} years",
            "salary_forecast": {
                f"year_{i+1}": forecast for i, forecast in enumerate(forecasts[:years_ahead])
            },
            "growth_rate": round(((forecasts[-1] - forecasts[0]) / forecasts[0]) * 100, 1),
            "confidence": "Medium (based on industry trends)"
        }

    def _prepare_features(self, job_features: Dict[str, Any]) -> List[float]:
        """Prepare features for model prediction"""
        features = []

        # Experience years
        features.append(job_features.get('experience_years', 2))

        # Skill count
        skills = job_features.get('skills', [])
        features.append(len(skills) if isinstance(skills, list) else 1)

        # Encoded categorical features
        for col in ['location', 'company_size', 'education', 'role_seniority']:
            value = job_features.get(col, 'unknown')
            if col in self.label_encoders:
                try:
                    encoded = self.label_encoders[col].transform([str(value)])[0]
                except:
                    # Handle unknown categories
                    encoded = 0
            else:
                encoded = 0
            features.append(encoded)

        return features

    def _fallback_prediction(self, job_features: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback prediction when model is not trained"""
        experience = job_features.get('experience_years', 2)
        skills = job_features.get('skills', [])
        skill_count = len(skills) if isinstance(skills, list) else 1

        # Simple rule-based prediction
        base_salary = 600000  # Base for entry level
        experience_bonus = experience * 80000  # ₹80k per year
        skill_bonus = skill_count * 50000  # ₹50k per skill

        predicted = base_salary + experience_bonus + skill_bonus

        return {
            "predicted_salary": round(predicted, -3),
            "confidence_interval": {
                "lower": round(predicted * 0.8, -3),
                "upper": round(predicted * 1.2, -3)
            },
            "confidence_level": "Low (fallback model)",
            "currency": "INR",
            "method": "Rule-based estimation",
            "factors_influencing": [
                f"{experience} years experience",
                f"{skill_count} technical skills",
                "Location and role factors"
            ]
        }

    def _calculate_confidence_level(self, coefficient_of_variation: float) -> str:
        """Calculate confidence level based on prediction variance"""
        if coefficient_of_variation < 0.1:
            return "Very High"
        elif coefficient_of_variation < 0.2:
            return "High"
        elif coefficient_of_variation < 0.3:
            return "Medium"
        elif coefficient_of_variation < 0.4:
            return "Low"
        else:
            return "Very Low"

    def _explain_prediction(self, job_features: Dict[str, Any]) -> List[str]:
        """Explain what factors influenced the prediction"""
        factors = []

        experience = job_features.get('experience_years', 0)
        if experience > 0:
            factors.append(f"{experience} years of experience")

        skills = job_features.get('skills', [])
        if skills:
            factors.append(f"{len(skills)} relevant skills")

        location = job_features.get('location', '')
        if location:
            factors.append(f"Location: {location}")

        education = job_features.get('education', '')
        if education:
            factors.append(f"Education: {education}")

        return factors if factors else ["General market factors"]

    def _compare_to_market(self, prediction: float, job_features: Dict[str, Any]) -> Dict[str, Any]:
        """Compare prediction to market averages"""
        role = job_features.get('role', '').lower()
        experience = job_features.get('experience_years', 2)

        # Market averages (simplified)
        market_averages = {
            "data scientist": {1: 700000, 3: 950000, 5: 1300000, 8: 1800000},
            "software engineer": {1: 600000, 3: 850000, 5: 1200000, 8: 1600000},
            "renewable energy engineer": {1: 550000, 3: 750000, 5: 1100000, 8: 1500000},
            "sustainability manager": {1: 650000, 3: 900000, 5: 1250000, 8: 1700000}
        }

        market_avg = market_averages.get(role, market_averages.get("software engineer", {}))
        closest_exp = min(market_avg.keys(), key=lambda x: abs(x - experience))
        market_salary = market_avg.get(closest_exp, prediction)

        difference = ((prediction - market_salary) / market_salary) * 100

        if abs(difference) < 5:
            comparison = "At market rate"
        elif difference > 5:
            comparison = f"{abs(round(difference, 1))}% above market"
        else:
            comparison = f"{abs(round(difference, 1))}% below market"

        return {
            "market_comparison": comparison,
            "market_average": market_salary,
            "difference_percentage": round(difference, 1)
        }

    def _get_location_multiplier(self, location: str) -> float:
        """Get location-based salary multiplier"""
        location_multipliers = {
            "mumbai": 1.2,
            "delhi": 1.1,
            "bangalore": 1.15,
            "chennai": 1.05,
            "pune": 1.1,
            "hyderabad": 1.08,
            "kolkata": 0.95
        }
        return location_multipliers.get(location.lower(), 1.0)

    def _calculate_experience_bonus(self, years: int) -> float:
        """Calculate experience-based salary bonus"""
        if years <= 2:
            return 0
        elif years <= 5:
            return 0.2
        elif years <= 8:
            return 0.4
        else:
            return 0.6

# Global instance
salary_predictor = AdvancedSalaryPredictor()