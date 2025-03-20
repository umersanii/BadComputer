from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import os

app = Flask(__name__)
CORS(app)  # Allow all origins, or specify: CORS(app, resources={r"/api/*": {"origins": "http://192.168.1.29:3000"}})

def get_system_usage():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "temperature": get_temperature()
    }

def get_temperature():
    try:
        temp = os.popen("vcgencmd measure_temp").readline().strip()
        return float(temp.replace("temp=", "").replace("'C", ""))
    except:
        return 0.0  # Return 0.0 if temperature can't be fetched

@app.route('/api/usage', methods=['GET'])
def usage():
    return jsonify(get_system_usage())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
