"""
This file contains the application's Flask web server, which manages and provides access to the different website routes.
"""

from http import server
from flask import Flask
from flask import render_template, request, redirect, url_for, session
import requests
import json
import datetime
import quotation_algorithm as quote
import random
import string

app = Flask(__name__)

# Setting session key
app.secret_key = "password"


@app.route("/index", methods=["GET", "POST"])
@app.route("/")
def index():
    """Returns the application's index page."""
    return render_template("index.html")


@app.route("/booking")
def bookings():
    """Returns the application's bookings page."""
    return render_template("booking.html")


@app.route("/booking/removals", methods=["POST", "GET"])
def booking_removals():
    """Flask creates a POST request that is enabled
    through HTML only if the user is logged in, the
    request creates a new product using the SQL Rest
    API
    """
    if request.method == "POST":
        # Retrieving current time
        current_time = datetime.datetime.now()

        # Refactoring 'current_time' into "DAY/MONTH/YEAR HOUR/MIN/SECOND"
        current_time_string = current_time.strftime("%d/%m/%Y %H:%M:%S")

        # Required service requirements
        service_requirements = {
            "booking_date": current_time_string,
            "vehicle_type": "TBD",
            "service_cycles": 0,
            "service_date": request.form["inputDate"],
            "service_type": "Removals service",
            "service_time": request.form["inputTime"],
            "pick_up_location": request.form["inputPickup"],
            "drop_off_location": request.form["inputDropoff"],
            "customer_id": request.form["inputCustomerID"],
            "employee_id": 1,
        }

        # Specific service requirements
        service_characteristics = {
            # Bedroom
            "Single bed": request.form["inputSingleBed"],
            "Double bed": request.form["inputDoubleBed"],
            "King-size bed": request.form["inputKingSizeBed"],
            "Wardrobe": request.form["inputWardrobe"],
            "Drawers": request.form["inputDrawers"],
            "Bedside table": request.form["inputBedsideTable"],
            "Dressing table": request.form["inputDressingTable"],
            "Desk": request.form["inputDesk"],
            "Office chair": request.form["inputOfficeChair"],
            "Artwork": request.form["inputArtwork"],
            # Livingroom
            "Sofa": request.form["inputSofa"],
            "Armchair": request.form["inputArmchair"],
            "Coffe table": request.form["inputCoffeTable"],
            "Television": request.form["inputTelevision"],
            "TV stand": request.form["inputTVStand"],
            "Book case": request.form["inputBookCase"],
            # Kitchen
            "Fridge freezer": request.form["inputFridgeFreezer"],
            "Washing machine": request.form["inputWashingMachine"],
            "Microwave": request.form["inputMicrowave"],
            "Cooker": request.form["inputCooker"],
            "Dishwasher": request.form["inputDishwasher"],
            "Kitchen table": request.form["inputKitchenTable"],
            "Dinning table": request.form["inputDinningTable"],
            "Dinning chair": request.form["inputDinningChair"],
            # Bathroom
            "Mirror": request.form["inputMirror"],
            "Rug": request.form["inputRug"],
            "Bathroom tub": request.form["inputBathroomTub"],
            "Bathroom cabinet": request.form["inputBathroomCabinet"],
            # Boxes and packaging
            "Box": request.form["inputBox"],
            "Suit case": request.form["inputSuitCase"],
        }

        # Filtering specific_service_requirements to drop null values
        curated_service_requirements = {}

        for k in service_characteristics:
            if service_characteristics[k] != "":
                curated_service_requirements[k] = service_characteristics[k]

        service_requirements["serviceCharacteristics"] = curated_service_requirements

        session["serviceRequirements"] = service_requirements

        return redirect(url_for("payment"))

    else:
        return render_template("removals_service.html")


@app.route("/payment", methods=["GET", "POST"])
def payment():
    # Making session data accessible
    booking_data = session["serviceRequirements"]

    quote_data = {
        "amount": 1.00,
        "transaction_outcome": "Payment due",
    }

    def random_string(letter_count, digit_count):
        str1 = "".join(
            (random.choice(string.ascii_letters) for x in range(letter_count))
        )
        str1 = "".join((random.choice(string.digits) for x in range(digit_count)))

        sam_list = list(str1)  # Converts the string to a list.
        random.shuffle(
            sam_list
        )  # Uses a random.shuffle() function to shuffle the string.
        final_string = "".join(sam_list)
        return final_string

    random_booking_id = random_string(8, 4)
    random_payment_id = random_string(8, 4)

    quote.complete_booking_details(
        quote_data,
        booking_data,
        quote.ITEMS_VOLUME,
        quote.VEHICLE_VOLUME_S,
        quote.VEHICLE_VOLUME_M,
        quote.VEHICLE_VOLUME_L,
    )

    # Creating a JSON object from booking_data
    final_booking_requirements = json.dumps(booking_data)
    final_quote_json = json.dumps(quote_data)
    data = json.loads(final_booking_requirements)
    final_quote_data = json.loads(final_quote_json)

    # Creating a String compatible with the API call
    service_characteristics_string = json.dumps(data["serviceCharacteristics"])

    if request.method == "POST":
        requests.post(
            "http://127.0.0.1:8080/booking/new",
            json={
                "payment_id": random_payment_id,
                "payment_amount": quote_data["amount"],
                "payment_outcome": quote_data["transaction_outcome"],
                "booking_id": random_booking_id,
                "customer_id": booking_data["customer_id"],
                "employee_id": booking_data["employee_id"],
                "booking_date": booking_data["booking_date"],
                "vehicle_type": booking_data["vehicle_type"],
                "service_type": booking_data["service_type"],
                "service_date": booking_data["service_date"],
                "pick_up_location": booking_data["pick_up_location"],
                "drop_off_location": booking_data["drop_off_location"],
                "service_characteristics": service_characteristics_string,
                "service_cycles": booking_data["service_cycles"],
            },
        )

        return redirect(url_for("index"))  # TODO: Change for success message
    else:

        """Returns the application's bookings page."""
        if "booking_date" in booking_data:
            return render_template(
                "payment.html", data=data, quote_data=final_quote_data
            )
        else:
            return render_template("bookings.html")


@app.route("/login")
def login():
    """Returns the application's login page."""
    return render_template("login.html")


@app.route("/register")
def register():
    """Returns the application's register page."""
    return render_template("register.html")


@app.route("/account/bookings", methods=["GET"])
def account_bookings():
    """Returns the application's customer orders page."""
    return render_template("customer_bookings.html")


@app.route("/admin/login", methods=["GET"])
def admin_login():
    """Returns the application's admin page."""
    return render_template("admin_login.html")


@app.route("/admin/portal", methods=["GET", "POST"])
def admin_portal():
    """Returns the application's admin page."""
    if request.method == "POST":
        booking_id = request.form["delete-booking"]
        requests.delete(f"http://127.0.0.1:8080/bookings/delete/{booking_id}")
        return render_template("admin_portal.html")
    else:
        return render_template("admin_portal.html")


if __name__ == "__main__":
    app.run(debug=True)
