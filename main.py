import subprocess
import requests
import time
import psutil
import os
import json
from flask import Flask, jsonify, render_template
from flask_cors import CORS

NGROK_URL_FILE = "/home/umersani/Sani_Pi/ngrok_url.json"  # File to store API URL

app = Flask(__name__)
CORS(app)

def save_ngrok_url(url):
    """Save the latest ngrok URL to a file so the Discord bot can access it."""
    with open(NGROK_URL_FILE, "w") as f:
        json.dump({"ngrok_url": url}, f)

def get_ngrok_url():
    """Fetches the ngrok URL from its local API."""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        url = data['tunnels'][0]['public_url']
        save_ngrok_url(url)  # Save it for Discord bot
        return url
    except Exception as e:
        print("⚠️ Error fetching ngrok URL:", e)
        return None

def start_ngrok():
    """Starts ngrok and returns the public URL."""
    subprocess.Popen(["ngrok", "http", "5003", "--log=stdout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)  # Wait for ngrok to start
    return get_ngrok_url()

def get_system_usage():
    cpu_freq = psutil.cpu_freq()
    memory = psutil.virtual_memory()
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    
    return {
        "cpu_total": psutil.cpu_percent(interval=1),
        "cpu_per_core": psutil.cpu_percent(percpu=True),
        "cpu_freq": {
            "current": cpu_freq.current if cpu_freq else None,
            "min": cpu_freq.min if cpu_freq else None,
            "max": cpu_freq.max if cpu_freq else None
        },
        "memory": {
            "percent": memory.percent,
            "total": round(memory.total / (1024 ** 2), 2),  # MB
            "available": round(memory.available / (1024 ** 2), 2),
            "used": round(memory.used / (1024 ** 2), 2),
            "free": round(memory.free / (1024 ** 2), 2)
        },
        "disk": psutil.disk_usage('/').percent,
        "disk_io": {
            "read_mb": round(disk_io.read_bytes / (1024 * 1024), 2),
            "write_mb": round(disk_io.write_bytes / (1024 * 1024), 2)
        },
        "network": {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024 * 1024), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024 * 1024), 2)
        },
        "temperature": get_temperature(),
        "uptime": get_uptime()
    }

def get_uptime():
    """Get system uptime in seconds."""
    return round(time.time() - psutil.boot_time())

def get_temperature():
    try:
        temp = os.popen("vcgencmd measure_temp").readline().strip()
        return float(temp.replace("temp=", "").replace("'C", ""))
    except:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = float(f.read()) / 1000.0
                return temp
        except:
            return 45.0  # Default temperature

@app.route('/api/usage', methods=['GET'])
def usage():
    return jsonify(get_system_usage())

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    print("🚀 Starting Flask App...")
    time.sleep(2)  # Give ngrok time to start

    ngrok_url = start_ngrok()
    if ngrok_url:
        print(f"✅ Ngrok Public URL: {ngrok_url}")
        print(f"🌐 API Access: {ngrok_url}/api/usage")
    else:
        print("⚠️ Ngrok URL not available!")

    # This starts the Flask app
    app.run(host='0.0.0.0', port=5004)