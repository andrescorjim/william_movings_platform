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
    document.getElementById("loginModal").innerHTML = `
    
    `;
    let customer_id = user.uid;

    var element = document.querySelector('input[name="inputCustomerID"]');
    element.value = customer_id;
  } else {
    $(document).ready(function () {
      $("#loginModal").modal({ backdrop: "static", keyboard: false });
      $("#loginModal").modal("show");
    });
    document.getElementById("loginModal").innerHTML = `
    <div class="modal-dialog">
      <div class="modal-content py-4">
        <form id="login-form" style="max-width: 330px; margin: auto">
          <div class="text-center py-1">
            <h2>You must login before making a booking</h2>
            <label for="emailAddress" class="sr-only"></label>
            <input type="email" id="login-email" class="form-control mb-1" placeholder="Email Address" required autofocus />
            <label for="password" class="sr-only"></label>
            <input type="password" id="login-password" placeholder="Password" class="form-control mb-3" />
          </div>
          <div class="d-grid gap-2 mt-2">
            <button type="submit" class="btn btn-primary">Log in</button>
            <p class="fw-normal text-center text-muted mb-0">Or</p>
            <button type="button" class="btn btn-outline-dark" id="googlelogin">
              <i class="bi bi-google lead px-2"></i> Log in with Google </button>
          </div>
          <div class="text-center mt-4 mb-4">
            <a href="#" style="color: grey">I've forgotten my password</a>
          </div>
          <div class="text-center mt-3 pb-3">
            <p>New to William's Moving? <a href="/register">Create an account</a>
            </p>
          </div>
        </form>
      </div>
    </div>
    `;

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
          // const user = userCredential.user;
          // clear form
          loginForm.reset();

          // Refresh payment page
          window.location.href = "http://127.0.0.1:5000/booking/removals";
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          // ..
        });
    });
  }
});
