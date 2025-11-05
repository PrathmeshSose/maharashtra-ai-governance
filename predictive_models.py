from google.cloud import aiplatform
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import joblib
from config import Config

class PredictiveModels:
    def __init__(self):
        aiplatform.init(project=Config.PROJECT_ID, location=Config.REGION)
        self.models = {}
        self.encoders = {}
        
    def train_demand_predictor(self, data):
        """Train service demand prediction model"""
        # Encode categorical variables
        le_district = LabelEncoder()
        le_service = LabelEncoder()
        
        data['district_encoded'] = le_district.fit_transform(data['district'])
        data['service_encoded'] = le_service.fit_transform(data['service_type'])
        
        # Features and target
        features = ['district_encoded', 'service_encoded', 'month', 'day_of_week', 'resolution_time']
        X = data[features]
        y = data['request_count']
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Store model and encoders
        self.models['demand_predictor'] = model
        self.encoders['district'] = le_district
        self.encoders['service'] = le_service
        
        return model.score(X, y)
    
    def predict_service_demand(self, district, service_type, month, day_of_week, avg_resolution_time):
        """Predict future service demand"""
        if 'demand_predictor' not in self.models:
            return None
            
        # Encode inputs
        district_encoded = self.encoders['district'].transform([district])[0]
        service_encoded = self.encoders['service'].transform([service_type])[0]
        
        # Make prediction
        features = np.array([[district_encoded, service_encoded, month, day_of_week, avg_resolution_time]])
        prediction = self.models['demand_predictor'].predict(features)[0]
        
        return max(0, int(prediction))
    
    def calculate_priority_score(self, request_count, population, urgency_level):
        """Calculate dynamic priority score"""
        base_score = (request_count / population) * 100
        urgency_multiplier = {'low': 1.0, 'medium': 1.5, 'high': 2.0, 'critical': 3.0}
        
        return min(100, base_score * urgency_multiplier.get(urgency_level, 1.0))
    
    def save_models(self):
        """Save trained models"""
        for name, model in self.models.items():
            joblib.dump(model, f'{name}.pkl')
        for name, encoder in self.encoders.items():
            joblib.dump(encoder, f'{name}_encoder.pkl')
    
    def load_models(self):
        """Load saved models"""
        try:
            self.models['demand_predictor'] = joblib.load('demand_predictor.pkl')
            self.encoders['district'] = joblib.load('district_encoder.pkl')
            self.encoders['service'] = joblib.load('service_encoder.pkl')
        except FileNotFoundError:
            print("Models not found. Train models first.")