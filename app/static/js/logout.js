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

// On auth state changes
const auth = getAuth().onAuthStateChanged((user) => {
  if (user) {
    document.getElementById("loginBtn").style.cssText = "display: none;";
    document.getElementById("registerBtn").style.cssText = "display: none;";

    //logout event
    const logout = document.getElementById("logoutBtn");
    logout.addEventListener("click", (e) => {
      e.preventDefault();
      const auth = getAuth();
      signOut(auth)
        .then(() => {
          // Sign-out successful.
          document.getElementById("bookingsBtn").style.cssText = "display: none;";
          document.getElementById("loginBtn").style.cssText = "";
          document.getElementById("registerBtn").style.cssText = "";
          // redirect to index page
          window.location.href = "http://127.0.0.1:5000/";
        })

        .catch((error) => {
          // An error happened.
        });
    });
  } else {
    document.getElementById("bookingsBtn").style.cssText = "display: none;";
    document.getElementById("logoutBtn").style.cssText = "display: none;";
    document.getElementById("divider").style.cssText = "display: none;";
    document.getElementById("loginBtn").style.cssText = "";
    document.getElementById("registerBtn").style.cssText = "";
  }
});
