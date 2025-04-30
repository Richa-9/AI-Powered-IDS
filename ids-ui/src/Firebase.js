// src/Firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore, collection, addDoc } from 'firebase/firestore';


// Optional: Remove this if you're not using analytics
// import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
<<<<<<< HEAD
    apiKey: "AIzaSyAItBlwKD0d92-AeTEOu_xzg-YxHMvjbZI",
=======
    apiKey: "Your API key",
>>>>>>> 08e62031fad3de1b1497fa7463195959a68653b6
    authDomain: "ai-powered-ids.firebaseapp.com",
    projectId: "ai-powered-ids",
    storageBucket: "ai-powered-ids.firebasestorage.app",
    messagingSenderId: "908535762376",
    appId: "1:908535762376:web:f62d985d761e60f430c4fd",
    measurementId: "G-ZEBMQ5NVCL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and export it
const auth = getAuth(app);
export const db = getFirestore(app);

<<<<<<< HEAD
export { auth };
=======
export { auth };
>>>>>>> 08e62031fad3de1b1497fa7463195959a68653b6
