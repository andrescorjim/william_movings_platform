// Import the functions you need from the SDKs you need
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
  apiKey: "AIzaSyDqB3vTFrfsiLnHr86281HK-eA5iAcKT_k",
  authDomain: "wm-auth.firebaseapp.com",
  projectId: "wm-auth",
  storageBucket: "wm-auth.appspot.com",
  messagingSenderId: "578630150947",
  appId: "1:578630150947:web:181dc89cc98288fa4f7a96",
  measurementId: "G-FGZ5ZT8Y3C",
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
      window.location.href = "http://127.0.0.1:5000/";
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // ..
    });
});

// Google login
const googleButton = document.querySelector("#googlelogin");
googleButton.addEventListener("click", (e) => {
  const auth = getAuth();
  signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access the Google API.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      // The signed-in user info.
      const user = result.user;
      // ...
    })
    .catch((error) => {
      // Handle Errors here.
      const errorCode = error.code;
      const errorMessage = error.message;
      // The email of the user's account used.
      const email = error.email;
      // The AuthCredential type that was used.
      const credential = GoogleAuthProvider.credentialFromError(error);
      // ...
    });
});
