import React, { useState } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom'; // import navigate
import { auth } from './Firebase';
import { db } from './Firebase'; // import Firestore
import { collection, addDoc } from 'firebase/firestore'; // Firestore functions
import './Auth.css';

const AdminSignup = () => {
  const [name, setName] = useState(''); // new state for name
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // hook to navigate

  const handleSignup = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage("Passwords do not match ❌");
      return;
    }
    try {
      // Create user with Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // Save user data in Firestore
      await addDoc(collection(db, 'admins'), {
        name: name,
        email: email,
        uid: user.uid, // Save the UID to reference the user
      });

      setMessage('Admin account created successfully ✅');
      navigate('/dashboard'); // Redirect to dashboard after successful signup
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="admin-form">
      <h2>Admin Signup</h2>
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Admin Name"
          value={name}
          onChange={(e) => setName(e.target.value)} // handle name change
          required
        /><br />
        <input
          type="email"
          placeholder="Admin Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br />
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Create Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br />
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        /><br />
        <label>
          <input
            type="checkbox"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)}
          />
          Show Password
        </label><br />
        <button className="submit" type="submit">Sign Up</button>
      </form>
      {message && <p>{message}</p>}
      
      {/* Toggle to Login Page */}
      <p style={{ marginTop: '15px' }}>
        Already have an account?{' '}
        <button
          className="link-button"
          onClick={() => navigate('/')}
        >
          Login here
        </button>
      </p>
    </div>
  );
};

export default AdminSignup;