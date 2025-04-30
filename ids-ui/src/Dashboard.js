import React, { useEffect, useRef, useState } from "react";
import './Dashboard.css';
import { Bar } from "react-chartjs-2";
import { io } from "socket.io-client";
import { useNavigate } from "react-router-dom"; // Import the useNavigate hook for navigation
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

const Dashboard = () => {
  const [trafficData, setTrafficData] = useState([]);
  const [counts, setCounts] = useState({
    Malicious: 0,
    Genuine: 0,
    "False Positive": 0,
    "False Negative": 0,
  });
  const canvasRef = useRef(null);
  const navigate = useNavigate(); // Initialize the useNavigate hook

  useEffect(() => {
    // Starry background
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    const stars = Array.from({ length: 500 }).map(() => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 1.5,
      alpha: Math.random(),
      delta: Math.random() * 0.02,
    }));

    const animateStars = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let star of stars) {
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
        ctx.fill();

        star.alpha += star.delta;
        if (star.alpha <= 0 || star.alpha >= 1) {
          star.delta = -star.delta;
        }
      }
      requestAnimationFrame(animateStars);
    };
    animateStars();
  }, []);

  useEffect(() => {
    const socket = io("http://localhost:5001"); // Or your backend URL/IP

    socket.on("new_traffic", (data) => {
      setTrafficData((prev) => [data, ...prev]);

      setCounts((prev) => {
        const updated = { ...prev };
        if (data.Reason === "Correct" && data.Prediction === "Malicious") updated["Malicious"]++;
        else if (data.Reason === "Correct" && data.Prediction === "Normal") updated["Genuine"]++;
        else if (data.Reason === "False Positive") updated["False Positive"]++;
        else if (data.Reason === "False Negative") updated["False Negative"]++;
        return updated;
      });
    });

    return () => socket.disconnect();
  }, []);

  const chartData = {
    labels: ["Malicious", "Genuine", "False Positive", "False Negative"],
    datasets: [
      {
        label: "Number of Packets",
        data: [
          counts["Malicious"],
          counts["Genuine"],
          counts["False Positive"],
          counts["False Negative"],
        ],
        backgroundColor: ["#ef5350", "#66bb6a", "#fdd835", "#e57373"],
        borderColor: ["#b71c1c", "#1b5e20", "#fbc02d", "#c62828"],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { labels: { color: "#ccc" } },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { color: "#ccc" },
        grid: { color: "#333" },
        title: {
          display: true,
          text: "Number of Packets",
          color: "#ccc",
        },
      },
      x: {
        ticks: { color: "#ccc" },
        grid: { color: "#333" },
        title: {
          display: true,
          text: "Prediction",
          color: "#ccc",
        },
      },
    },
  };

  const getRowClass = (data) => {
    if (data.Reason === "Correct") return data.Prediction === "Malicious" ? "malicious" : "normal";
    if (data.Reason === "False Positive") return "false-positive";
    if (data.Reason === "False Negative") return "false-negative";
    return "";
  };

  // Log out functionality
  const handleLogout = () => {
    console.log("Logout clicked!");  // Check if this is printed in the console

    // Clear any session or authentication data
    localStorage.removeItem('authToken');  // Adjust this if you store token or user data elsewhere

    // Redirect to login page
    navigate("/"); // Use navigate instead of history.push
  };

  return (
    <div>
      <canvas id="starCanvas" ref={canvasRef} className="star-canvas" />

      <h1 className="dashboard-title">AI Powered Real-Time Intrusion Detection System</h1>

      {/* Log Out Button */}
      <button onClick={handleLogout} className="logout-button">Log Out</button>

      <div id="chartContainer" className="chart-container">
        <div id="chartTitle" className="chart-title">Traffic Prediction Overview</div>

        <Bar data={chartData} options={chartOptions} height={100} />
      </div>

      <table className="traffic-table">
        <thead>
          <tr className="table-header">
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>Protocol</th>
            <th>Attack Type</th>
            <th>Prediction</th>
            <th>Ground Truth</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>
          {trafficData.map((row, index) => (
            <tr key={index} className={`fade-in ${getRowClass(row)}`}>
              <td>{row["Source IP"]}</td>
              <td>{row["Destination IP"]}</td>
              <td>{row["Protocol"]}</td>
              <td>{row["Attack Type"]}</td>
              <td>{row["Prediction"]}</td>
              <td>{row["Ground Truth"]}</td>
              <td>{row["Reason"]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

<<<<<<< HEAD
export default Dashboard;
=======
export default Dashboard;
>>>>>>> 08e62031fad3de1b1497fa7463195959a68653b6
