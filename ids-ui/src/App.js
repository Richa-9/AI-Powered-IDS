import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./Dashboard"; // Import the Dashboard Component
import Login from "./Login"; // Import the Login Component
import Signup from "./Signup"; // Import the Signup Component

function App() {
  return (
    <Router>
      <Routes>
        {/* Route for the Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* Route for the Login page */}
        <Route path="/" element={<Login />} />
        
        {/* Route for the Signup page */}
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;