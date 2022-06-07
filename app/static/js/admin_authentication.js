import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.4.1/firebase-analytics.js";

// SDKs for Firebase products used
// https://firebase.google.com/docs/web/setup#available-libraries
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  signInWithPopup,
  GoogleAuthProvider,
} from "https://www.gstatic.com/firebasejs/9.4.1/firebase-auth.js";

// Firebase project-specific configuration
const firebaseConfig = {
  apiKey: "AIzaSyDm6RgkQ5aJ6ty3G0x6q4tUqvsaMgQ6GeA",
  authDomain: "wm-admin-portal.firebaseapp.com",
  projectId: "wm-admin-portal",
  storageBucket: "wm-admin-portal.appspot.com",
  messagingSenderId: "1077573687576",
  appId: "1:1077573687576:web:c0bd30b038ea1028d9266d",
  measurementId: "G-2JWWMY8NSY",
};

// Firebase services initialization
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const provider = new GoogleAuthProvider();

// Login event
const loginForm = document.querySelector("#login-form");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  // Capture inputs from login form
  const email = document.querySelector("#login-email").value;
  const password = document.querySelector("#login-password").value;

  const auth = getAuth();
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      // clear form
      loginForm.reset();
      // Redirect URL after signup succesfully
      window.location.href = "http://127.0.0.1:5000/admin/portal";
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // ..
    });
});
