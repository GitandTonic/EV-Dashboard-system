import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

class BatteryHealthModel:
    def __init__(self):
        self.model = None
        self.load_or_train_model()
        
    def load_or_train_model(self):
        model_path = 'battery_health_model.joblib'
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.train_model()
            joblib.dump(self.model, model_path)
    
    def train_model(self):
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 10000
        
        # Simulate realistic parameter ranges
        temperature = np.random.uniform(20, 50, n_samples)
        dod = np.random.uniform(10, 95, n_samples)
        c_rate = np.random.uniform(0.5, 2.5, n_samples)
        inclination = np.random.uniform(-15, 15, n_samples)
        load = np.random.uniform(50, 300, n_samples)
        jerk = np.random.uniform(0.1, 3.0, n_samples)
        
        # Calculate health based on weighted factors
        # These weights are based on research about battery degradation factors
        health = 100 - (
            0.4 * np.clip((temperature - 25) / 25 * 15, 0, 15) +  # Temperature effect (up to 15% degradation)
            0.3 * np.clip((dod - 20) / 75 * 20, 0, 20) +          # DOD effect (up to 20% degradation)
            0.2 * np.clip((c_rate - 0.5) / 2 * 10, 0, 10) +       # C-rate effect (up to 10% degradation)
            0.05 * np.clip(np.abs(inclination) / 15 * 5, 0, 5) +   # Inclination effect (up to 5% degradation)
            0.03 * np.clip((load - 50) / 250 * 5, 0, 5) +          # Load effect (up to 5% degradation)
            0.02 * np.clip(jerk / 3 * 5, 0, 5)                     # Jerk effect (up to 5% degradation)
        )
        
        # Calculate remaining distance (km)
        # Base distance of 400km at full health, reduced by degradation factors
        base_distance = 400
        remaining_distance = base_distance * (health / 100) * (
            0.9 + 0.1 * (25 / np.clip(temperature, 25, 50)) *  # Temperature effect
            (1 - 0.2 * (np.clip(dod, 20, 95) - 20) / 75) *     # DOD effect
            (1 - 0.1 * (np.clip(c_rate, 0.5, 2.5) - 0.5) / 2)  # C-rate effect
        )
        
        X = np.column_stack([temperature, dod, c_rate, inclination, load, jerk])
        y = np.column_stack([health, remaining_distance])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Print model performance
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Model trained. Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
    
    def predict(self, temperature, dod, c_rate, inclination, load, jerk):
        features = np.array([[temperature, dod, c_rate, inclination, load, jerk]])
        prediction = self.model.predict(features)[0]
        
        return {
            'health': max(0, min(100, round(prediction[0], 1))),
            'remaining_distance': max(0, round(prediction[1], 1))
        }