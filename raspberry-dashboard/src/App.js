import React, { useState, useEffect } from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import "./index.css";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";


const UsageDashboard = () => {
  const [usage, setUsage] = useState({ cpu: 0, memory: 0, disk: 0, temperature: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsage = async () => {
      try {
        const response = await fetch("http://192.168.1.29:5000/api/usage");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched data:", data); // Debugging output
        setUsage(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching usage data:", error);
        setLoading(false); // Ensure loading is updated even if there is an error
      }
    };
    

    fetchUsage();
    const interval = setInterval(fetchUsage, 2000);
    return () => clearInterval(interval);
  }, []);


  const history = []; // Initialize history variable to avoid 'Unexpected use of history' error

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-6">Raspberry Pi Usage Dashboard</h1>
      {loading ? (
        <p className="text-lg">Loading data...</p>
      ) : (
        <div className="flex flex-wrap justify-center gap-4 w-full max-w-4xl"
        style={{ display: "flex", justifyContent: "center", gap: "20px", padding: "20px" }}
        >
          {["cpu", "memory", "disk", "temperature"].map((key) => (
            <div
              key={key}
              className="bg-gray-800 p-4 rounded-xl shadow-md flex flex-col items-center w-40"
            >
              <h2 className="text-sm font-semibold mb-2">{key.toUpperCase()}</h2>
              <div className="w-20 h-20"
              style={{ width: 240, flex: 1, display: "flex", justifyContent: "center", alignItems: "center" , flexDirection: "row" }}
              >
                <CircularProgressbar
                  value={usage[key] || 0}
                  text={`${usage[key] || 0}%`}
                  styles={buildStyles({
                    textColor: "#fff",
                    pathColor: key === "temperature" ? "#ff5733" : "#4ade80",
                    trailColor: "#374151",
                  })}
                />
              </div>
            </div>
          ))}
        </div>
      )}

<div className="w-full max-w-5xl mt-6">
            <h2 className="text-xl font-semibold mb-4">Usage History</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" stroke="#fff" />
                <YAxis domain={[0, 100]} stroke="#fff" />
                <Tooltip contentStyle={{ backgroundColor: "#333", color: "#fff" }} />
                <Line type="monotone" dataKey="cpu" stroke="#4ade80" name="CPU Usage" strokeWidth={2} />
                <Line type="monotone" dataKey="memory" stroke="#3b82f6" name="Memory Usage" strokeWidth={2} />
                <Line type="monotone" dataKey="disk" stroke="#facc15" name="Disk Usage" strokeWidth={2} />
                <Line type="monotone" dataKey="temperature" stroke="#ff5733" name="Temperature" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
    </div>

    
  );
  
};

export default UsageDashboard;
