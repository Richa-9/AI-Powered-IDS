import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom'; // import navigate
import { auth } from './Firebase';
import './Auth.css';

const AdminLogin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false); // new state for password visibility
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // hook to navigate

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      setMessage('Logged in as Admin 🎉');
      navigate('/dashboard'); // Redirect to dashboard after successful login
    } catch (error) {
      setMessage('Invalid credentials ❌');
    }
  };

  return (
    <div className="admin-form">
      <h2>Admin Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Admin Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br />
        
        <input
          type={showPassword ? "text" : "password"} // toggle password visibility
          placeholder="Admin Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br />
        
        {/* Show password checkbox */}
        <label>
          <input
            type="checkbox"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)} // toggle the password visibility state
          />
          Show Password
        </label><br />
        
        <button className="submit" type="submit">Log In</button>
      </form>
      {message && <p>{message}</p>}

      {/* Toggle to Signup Page */}
      <p style={{ marginTop: '15px' }}>
        Don't have an account?{' '}
        <button
          className="link-button"
          onClick={() => navigate('/signup')}
        >
          Sign up here
        </button>
      </p>
    </div>
  );
};

export default AdminLogin;