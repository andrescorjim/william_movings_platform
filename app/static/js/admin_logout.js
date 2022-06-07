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
          // Editing My Account's functionality
          document.getElementById("bookingsBtn").style.cssText = "display: none;";
          document.getElementById("loginBtn").style.cssText = "";
          document.getElementById("registerBtn").style.cssText = "";
          // redirect to admin portal page
          window.location.href = "http://127.0.0.1:5000/admin/login";
        })
        .catch((error) => {
          // An error happened.
        });
    });
  } else {
    // Editing account's functionality
    document.getElementById("bookingsBtn").style.cssText = "display: none;";
    document.getElementById("logoutBtn").style.cssText = "display: none;";
    document.getElementById("divider").style.cssText = "display: none;";
    document.getElementById("loginBtn").style.cssText = "";
    document.getElementById("registerBtn").style.cssText = "";
  }
});
