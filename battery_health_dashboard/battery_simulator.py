import random
import time
from datetime import datetime, timedelta

class BatterySimulator:
    def __init__(self):
        self.initial_health = 100  # Starting with 100% health
        self.current_health = self.initial_health
        self.history = []
        
    def generate_data(self):
        # Simulate realistic battery parameters
        temperature = round(random.uniform(25, 45), 1)  # °C
        dod = random.randint(10, 95)  # Depth of Discharge %
        c_rate = round(random.uniform(0.5, 2.5), 1)  # Charge/Discharge rate
        inclination = random.randint(-15, 15)  # degrees
        load = random.randint(50, 300)  # kg
        jerk = round(random.uniform(0.1, 3.0), 1)  # m/s³
        
        # Calculate energy consumption based on parameters
        base_consumption = 5.0  # kWh
        load_factor = load / 100  # 1-3x
        inclination_factor = 1 + abs(inclination) / 45  # 1-1.33x
        jerk_factor = 1 + jerk / 5  # 1-1.6x
        
        power_consumption = round(base_consumption * load_factor * inclination_factor * jerk_factor, 1)
        
        # Calculate health degradation
        health_degradation = self.calculate_health_degradation(temperature, dod, c_rate, jerk)
        self.current_health = max(0, min(100, self.current_health - health_degradation))
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'temperature': temperature,
            'dod': dod,
            'c_rate': c_rate,
            'inclination': inclination,
            'load': load,
            'jerk': jerk,
            'power_consumption': power_consumption,
            'health': round(self.current_health, 1),
            'voltage': round(random.uniform(45, 52), 1),  # V
            'current': round(random.uniform(50, 200), 1),  # A
        }
        
        self.history.append(data)
        if len(self.history) > 1000:  # Keep only recent history
            self.history = self.history[-1000:]
            
        return data
    
    def calculate_health_degradation(self, temperature, dod, c_rate, jerk):
        # Health degradation factors (per reading)
        temp_factor = max(0, (temperature - 30) / 1000)  # 0.015% degradation at 45°C
        dod_factor = (dod - 20) / 5000 if dod > 20 else 0  # 0.015% degradation at 95% DOD
        c_rate_factor = (c_rate - 1) / 2000  # 0.00075% degradation at 2.5C
        jerk_factor = jerk / 1000  # 0.003% degradation at 3.0 jerk
        
        return temp_factor + dod_factor + c_rate_factor + jerk_factor