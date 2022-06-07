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

    const api_bookings_url = "http://127.0.0.1:8080/bookings/" + user.uid;

    fetch(api_bookings_url)
      .then((response) => response.json())
      .then(function (response) {
        document.getElementById("output").innerHTML = `
                ${response
                  .map(function (data) {
                    const serviceCharacteristicsJson = JSON.parse(data.service_characteristics);

                    var serviceCharacteristicsEntries = "";
                    for (const [key, value] of Object.entries(serviceCharacteristicsJson)) {
                      serviceCharacteristicsEntries += `<small>${key}: <span class="text-muted">${value}</span></small><br>\n`;
                    }

                    var vehicleImageUrl = "";
                    switch (data.vehicle_type) {
                      case "Small vehicle":
                        vehicleImageUrl = "https://cvsvehiclegroup.co.uk/wp-content/uploads/2021/03/smallvan.jpg";
                        break;
                      case "Medium vehicla":
                        vehicleImageUrl =
                          "https://purepng.com/public/uploads/large/purepng.com-vantruckvehicletransportwhitevanbuscargodeliveryautocommercialcourier-981525067770rld6a.png";
                        break;
                      case "Large vehicle":
                        vehicleImageUrl =
                          "https://static.wixstatic.com/media/fdaab4_375347272af043f6bbe60ecf6c2a9e52~mv2.png/v1/fill/w_486,h_382,al_c,q_85,usm_4.00_1.00_0.00,enc_auto/New%20Ford%20Transit%20Luton.png";
                        break;
                      default:
                        vehicleImageUrl = "not recognised...";
                    }
                    return `
                    <div class="card orders-card mb-3">
                      <div class="card-header">
                        <ul class="nav nav-tabs card-header-tabs">
                          <li class="nav-item">
                            <a class="nav-link active" aria-current="true" href="#">Booking</a>
                          </li>
                          <li class="nav-item">
                            <a class="nav-link disabled" href="#">Track booking</a>
                          </li>
                          <li class="nav-item">
                            <a class="nav-link disabled">Modify booking</a>
                          </li>
                          <li class="nav-item">
                            <a class="nav-link disabled">Cancel booking</a>
                          </li>
                        </ul>
                      </div>
                      <div class="row">
                        <div class="col">
                          <div class="card-body">
                            <div class="card-body-title">
                              <div class="row">
                                <div class="col-3">
                                  <p class="fw-bold">Booking ID: <span class="fw-light">${data.booking_id}</span>
                                  </p>
                                </div>
                                <div class="col-3">
                                  <p class="fw-bold">Booking Date: <span class="fw-light">${data.booking_date}</span>
                                  </p>
                                </div>
                                <div class="col-2">
                                  <p class="fw-bold">Carrier: <span class="fw-light">${data.employee_name}</span>
                                  </p>
                                </div>
                                <div class="col-3">
                                  <p class="fw-bold">Carrier Contact: <span class="fw-light">${data.employee_phone_number}</span>
                                  </p>
                                </div>
                                <hr>
                              </div>
                            </div>
                            <div class="row mt-3">
                              <div class="col-3">
                                <img src="${vehicleImageUrl}" class="img-fluid" style="border-radius: 15px; width: 100%; height: auto; background-size: contain" />
                              </div>
                              <div class="col-3">
                                <p class="fw-bold text-left">Service type: <span class="fw-light">${data.service_type}</span>
                                </p>
                                <p class="fw-bold text-left">Service date: <span class="fw-light">${data.service_date}</span>
                                </p>
                                <p class="fw-bold text-left">Pick up location: <span class="fw-light">${data.pick_up_location}</span>
                                </p>
                                <p class="fw-bold text-left">Drop off location: <span class="fw-light">${data.drop_off_location}</span>
                                </p>
                                <p class="fw-bold">Total: <span class="fw-light">${data.payment_amount}</span>
                                </p>
                                <p class="fw-bold">Payment outcome: <span class="fw-light">${data.payment_outcome}</span>
                                </p>
                              </div>
                              <div class="col-5">
                                <div class="accordion mb-3" id="accordionFlushExample" style="margin-top:0;">
                                  <div class="accordion-item">
                                    <h2 class="accordion-header" id="flush-headingOne">
                                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                                        <h6 class="my-0">Your inventory</h6>
                                      </button>
                                    </h2>
                                    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
                                      <div class="accordion-body">
                                        ${serviceCharacteristicsEntries}
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    `;
                  })
                  .join("")}
                `;
      });
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
            <h2>You must login before viewing your booking</h2>
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
          // clear form
          loginForm.reset();

          // Refresh payment page
          window.location.href = "http://127.0.0.1:5000/account/bookings";
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          // ..
        });
    });
  }
});
