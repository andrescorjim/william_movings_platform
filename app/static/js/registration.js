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

// Sign-up event
const signupForm = document.querySelector("#signup-form");

signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  //Capture inputs from signup form
  const name = signupForm.querySelector("#customer-name").value;
  const email = document.querySelector("#signup-email").value;
  const phone_number = signupForm.querySelector("#customer-phone").value;
  const password = document.querySelector("#signup-password").value;

  const auth = getAuth();
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Registered user

      try {
        // Make API call to create a new user
        // Preparing JSON string
        var data = JSON.stringify({
          customer_id: userCredential.user.uid, // TODO: get user id
          customer_name: name,
          customer_email: email,
          customer_phone_number: phone_number,
        });

        // Preparing XMLHttpRequest
        var xhr = new XMLHttpRequest();
        var url = "http://127.0.0.1:8080/newuser";
        xhr.open("POST", url);
        xhr.setRequestHeader("Content-Type", "application/json");

        // Making request
        xhr.send(data);

        // clear form
        signupForm.reset();
      } catch (ex) {
        console.log(ex);
      }
      // Send user back to home page
      window.location.href = "http://127.0.0.1:5000/";
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // ..
    });
});

// On auth state changes
const auth = getAuth().onAuthStateChanged((user) => {
  if (user) {
    // Display when the user is logged in
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
