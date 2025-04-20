import subprocess
import requests
import time
import psutil
import os
import json
from flask import Flask, jsonify, render_template, make_response
import socket
from pyngrok import ngrok
from passw import TOKEN  

NGROK_URL_FILE = "/home/umersani/BadComputer/ngrok_url.json"  # File to store API URL

app = Flask(__name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def get_swap_memory():
    """Returns swap memory usage information for Raspberry Pi"""
    swap = psutil.swap_memory()
    return {
        'total': round(swap.total / (1024 ** 2), 1),  # Convert to MB
        'used': round(swap.used / (1024 ** 2), 1),    # Convert to MB
        'free': round(swap.free / (1024 ** 2), 1),    # Convert to MB
        'percent': round(swap.percent, 1)
    }

def get_ip_address():
    """Get the local IP address of the Raspberry Pi"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_hostname():
    """Get the hostname of the Raspberry Pi"""
    try:
        return subprocess.check_output(['hostname']).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting hostname: {e}")
        return "Unknown"

def get_mac_address():
    """Get the MAC address of the Raspberry Pi"""
    try:
        mac = open('/sys/class/net/eth0/address').read()
        return mac.strip()
    except Exception as e:
        print(f"❌ Error getting MAC address: {e}")
        return "00:00:00:00:00:00"
    


def save_ngrok_url(url):
    """Save the latest ngrok URL to a file so it can be accessed by other services."""
    try:
        with open(NGROK_URL_FILE, "w") as f:
            json.dump({"ngrok_url": url}, f)
            print(url)
    except Exception as e:
        print(f"❌ Error saving ngrok URL to file: {e}")

def get_ngrok_url():
    """Fetches the ngrok URL from its local API, with retries."""
    for _ in range(10):  # Retry up to 10 times
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels")
            data = response.json()
            if "tunnels" in data and len(data["tunnels"]) > 0:
                url = data["tunnels"][0]["public_url"]
                save_ngrok_url(url)  # Save it for future use
                return url
        except Exception as e:
            print("⚠️ Error fetching ngrok URL, retrying...", e)
        time.sleep(2)  # Wait before retrying
    print("❌ Ngrok URL could not be retrieved after multiple attempts!")
    return None

def start_ngrok():
    """Starts ngrok and returns the public URL."""
    try:
        ngrok.set_auth_token(TOKEN)  # Replace with your actual token
        tunnel = ngrok.connect(5004, bind_tls=True)  # Port on which Flask is running
        return tunnel.public_url
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None
def get_top_processes(n=5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc_info = proc.info
            if proc_info['cpu_percent'] is not None:
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:n]

def get_system_usage():
    """Fetch system stats like CPU, memory, disk, network, and temperature."""
    cpu_freq = psutil.cpu_freq()
    memory = psutil.virtual_memory()
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    swap = psutil.swap_memory()

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
            "free": round(memory.free / (1024 ** 2), 2),
            'swap_total': round(swap.total / (1024 ** 2), 1),
            'swap_used': round(swap.used / (1024 ** 2), 1),
            'swap_free': round(swap.free / (1024 ** 2), 1),
            'swap_percent': round(swap.percent, 1)
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
        "uptime": get_uptime(),
        "data": {
            'top_processes': get_top_processes()
        },
        "ip_address": get_ip_address(),
        "hostname": get_hostname(),
        "mac_address": get_mac_address()
        
    }

def get_uptime():
    """Get system uptime in seconds."""
    return round(time.time() - psutil.boot_time())

def get_temperature():
    """Get the CPU temperature using system commands or files."""
    try:
        # Try using 'vcgencmd' for Raspberry Pi
        temp = os.popen("vcgencmd measure_temp").readline().strip()
        return float(temp.replace("temp=", "").replace("'C", ""))
    except Exception:
        try:
            # Fallback for Linux systems
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = float(f.read()) / 1000.0
                return temp
        except Exception:
            return 45.0  # Default temperature if both methods fail

@app.route('/api/usage', methods=['GET'])
def usage():
    """API endpoint to return system usage data."""
    try:
        response =  jsonify(get_system_usage())
        response.headers['ngrok-skip-browser-warning'] = 'true'
        print (response.headers)
        return response
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve system usage: {str(e)}"}), 500
    
@app.route('/favicon.ico')
def favicon():
    return "", 404  # Silently ignore

@app.after_request
def add_skip_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/')
def home():
    """Home route to display the dashboard with ngrok URL."""
    try:
        with open(NGROK_URL_FILE, 'r') as f:
            data = json.load(f)
        ngrok_url = data.get("ngrok_url", None)
        response = make_response(render_template('index.html', ngrok_url=ngrok_url))
        response.headers['ngrok-skip-browser-warning'] = '1'
        print (response.headers)
        return response
    except Exception as e:
        return jsonify({"error": f"Error loading ngrok URL: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask App...")

    # Start ngrok and retrieve the public URL
    ngrok_url = start_ngrok()
    if ngrok_url:
        print(f"✅ Ngrok Public URL: {ngrok_url}")
        print(f"🌐 API Access: {ngrok_url}/api/usage")
        save_ngrok_url(ngrok_url)  # Save the URL for future use
    else:
        print("⚠️ Ngrok URL not available!")

    # Start Flask app on correct port
    app.run(host='0.0.0.0', port=5004)

