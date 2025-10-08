from flask import Flask, render_template, jsonify
import threading
import time
from battery_simulator import BatterySimulator
from ml_model import BatteryHealthModel

app = Flask(__name__)
battery_simulator = BatterySimulator()
health_model = BatteryHealthModel()

# Global variable to store current battery data
current_data = battery_simulator.generate_data()

def update_data():
    """Background thread to update battery data every 2 seconds"""
    global current_data
    while True:
        time.sleep(2)
        current_data = battery_simulator.generate_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/battery-data')
def get_battery_data():
    global current_data
    health_prediction = health_model.predict(
        current_data['temperature'],
        current_data['dod'],
        current_data['c_rate'],
        current_data['inclination'],
        current_data['load'],
        current_data['jerk']
    )
    
    response_data = {
        **current_data,
        'health': health_prediction['health'],
        'remaining_distance': health_prediction['remaining_distance']
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    # Start background thread to update data
    update_thread = threading.Thread(target=update_data)
    update_thread.daemon = True
    update_thread.start()
    
    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False)