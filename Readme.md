# BadComputer - Raspberry Pi Resource Monitor

![BadComputer Dashboard](https://github.com/umersanii/SaniPi/blob/fb65a28dfca6d6de307e18dd6fa8388e7e19519c/Pi.jpeg)

## Overview

BadComputer is a sleek, real-time system resource monitoring dashboard designed specifically for Raspberry Pi devices. This web-based interface provides comprehensive information about your system's performance metrics in an intuitive and visually appealing format.

## Features

- **Real-time monitoring** of critical system metrics
- **CPU usage tracking** with per-core breakdown
- **Memory (RAM) monitoring** with detailed usage statistics
- **Swap memory usage** visualization
- **Storage** utilization and disk I/O metrics
- **Network traffic** monitoring
- **Temperature tracking** with historical graph
- **Process monitoring** showing top CPU-consuming processes
- **System information** display (uptime, IP, hostname, MAC address)
- **Intelligent alerts** for critical system states
- **Public URL access** via ngrok for remote monitoring
- **Responsive design** that works on desktop and mobile devices
- **Dark theme** with Batman-inspired styling


## Technologies Used

- **Backend:** 
  - Flask (Python web framework)
  - psutil library for system metrics
  - pyngrok for public URL tunneling
  - Flask-CORS for cross-origin resource sharing

- **Data Collection:** 
  - Real-time system metrics via psutil
  - Direct hardware access for temperature readings
  - Process monitoring capabilities

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/badcomputer.git
   cd badcomputer
   ```

2. Install the required dependencies:
   ```bash
   pip install flask flask-cors psutil pyngrok requests
   ```

3. Ensure you have ngrok installed and configured:
   ```bash
   pip install pyngrok
   ngrok authtoken YOUR_NGROK_AUTH_TOKEN
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the dashboard by navigating to:
   ```
   http://your-raspberry-pi-ip:5004
   ```
   
   Or use the ngrok URL for remote access (printed in the console when the app starts)

## Configuration

The application runs with sensible defaults, but you can modify the following:

### Backend Configuration (`app.py`)

- Update frequency (default: 5 seconds)
- Flask port (default: 5004)
- ngrok configuration and URL storage
- System metrics collection methods


### Alert Thresholds

Current alert thresholds are set to:
- CPU Usage: 80%
- Memory Usage: 80%
- Disk Usage: 90%
- Temperature: 70°C

## Directory Structure

```
badcomputer/
├── app.py               # Main Flask application
├── static/              # Static assets
│   ├── style.css        # Batman-themed dashboard styling
│   ├── batsy.png        # Logo image
│   └── bats.ico         # Favicon
├── templates/           # HTML templates
│   └── index.html       # Dashboard template
├── ngrok_url.json       # Stored ngrok URL for persistence
└── screenshots/         # Project screenshots
```

## API Endpoints

The dashboard provides the following API endpoints:

- `/api/usage` - Returns JSON with all system metrics including:
  - CPU usage (total and per-core)
  - Memory usage details
  - Disk usage and I/O
  - Network statistics
  - Temperature readings
  - Top processes by CPU usage
  - System information (hostname, IP, MAC address)

## Remote Access

BadComputer uses ngrok to create a secure tunnel to your Raspberry Pi, allowing you to access the dashboard from anywhere. The ngrok URL is:

- Displayed in the console when the application starts
- Stored in `ngrok_url.json` for persistence
- Accessible via the API at the application's root URL

## Design Details

The UI features a dark-themed Batman-inspired design with:

- Primary cyan accent color (`#00fff2`)
- Dark background with gradient effects
- Card-based dashboard layout
- Visual thermometer for temperature
- Animated progress bars with color-coding
- Responsive design for mobile devices
- Custom animations for "bat signal" effects

## Key CSS Features

- **Dynamic progress bars** that change color based on usage levels
- **Custom thermometer visualization** for temperature readings
- **Responsive grid layout** that adapts to different screen sizes
- **Batman-themed styling** with cyan accents and dark background
- **Animation effects** on cards and headers

## Backend Features

- **Process monitoring** to show top CPU-consuming processes
- **Hardware access** for accurate temperature readings
- **Network tunneling** via ngrok for remote access
- **Cross-origin support** via Flask-CORS
- **Error handling** for robust operation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Created by [Umer Sani](https://github.com/umersanii)
- Contributed by [Umer Ghafoor](https://github.com/umerghafoor)
- Inspired by Batman and various system monitoring tools
- Uses [Chart.js](https://www.chartjs.org/) for data visualization
- Uses [psutil](https://github.com/giampaolo/psutil) for system metrics
- Uses [pyngrok](https://github.com/alexdlaird/pyngrok) for tunneling

---
