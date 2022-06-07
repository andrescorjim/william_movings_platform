####
## Import libraries
####
from email.quoprimime import quote
import requests, json
import googlemaps
from googlemaps import convert
from math import ceil

# Placeholder data NOTE: Do not delete the placeholder data here
quote_data = {
    'amount': 1.00,
    'transaction_outcome': 'Payment due',
}

booking_data = {
    'booking_date': '20/05/2022 19:18:32', 
    'drop_off_location': 'Bournemouth, UK',
    'pick_up_location': 'London, UK',
    'serviceCharacteristics': {'Armchair': '2', 'Artwork': '1', 'Bathroom cabinet': '1', 'Bathroom tub': '1', 
                            'Bedside table': '1', 'Book case': '1', 'Box': '1', 'Coffe table': '1', 'Cooker': '1', 
                            'Desk': '1', 'Dinning chair': '1', 'Dinning table': '1', 'Dishwasher': '1', 
                            'Double bed': '1', 'Drawers': '1', 'Dressing table': '1', 'Fridge freezer': '1', 
                            'King-size bed': '1', 'Kitchen table': '1', 'Microwave': '1', 'Mirror': '1', 'Office chair': 
                            '1', 'Rug': '1', 'Single bed': '1', 'Sofa': '1', 'Suit case': '1', 'TV stand': '1', 
                            'Television': '1', 'Wardrobe': '1', 'Washing machine': '1'}, 
    'service_date': '2022-05-21', 
    'service_time': '20:18', 
    'service_type': 'Removals service', 
    'vehicle_type': 'TBD',
    'service_cycles': 0
}

# NOTE: More items can be added to this list if needed
ITEMS_VOLUME = {
        'Armchair': 10.4, 
        'Artwork': 2.3, 
        'Bathroom cabinet': 3.4, 
        'Bathroom tub': 60,
        'Bedside table': 4.6, 
        'Book case': 10.7, 
        'Box': 4.4, 
        'Coffe table': 4.8, 
        'Cooker': 31.4, 
        'Desk': 20.2, 
        'Dinning chair': 7.9, 
        'Dinning table': 18.3,
        'Dishwasher': 10.7, 
        'Double bed': 59.3, 
        'Drawers': 17, 
        'Dressing table': 24.7, 
        'Fridge freezer': 22.7, 
        'King-size bed': 70.5, 
        'Kitchen table': 20.4, 
        'Microwave': 3.3, 
        'Mirror': 0.1, 
        'Office chair': 11.7, 
        'Rug': 28.3, 
        'Single bed': 38.1, 
        'Sofa': 82.2, 
        'Suit case': 3.1, 
        'TV stand': 8.1, 
        'Television': 3.1, 
        'Wardrobe': 44.5, 
        'Washing machine': 10.7
}

####
## Calculating the storage volume of each vehicle type used by the company
####

VEHICLE_S_HEIGHT = 2.90026
VEHICLE_S_WIDTH = 3.333333
VEHICLE_S_LENGTH = 6.28937

VEHICLE_M_HEIGHT = 4.215879
VEHICLE_M_WIDTH = 5.544619
VEHICLE_M_LENGTH = 5.544619

VEHICLE_L_HEIGHT = 6.988189
VEHICLE_L_WIDTH = 6.528871
VEHICLE_L_LENGTH = 12.27034

# function to get volume from dimensions
def get_volume(width, height, length):
    """Returns the volume of an item"""
    volume = width * height * length
    return volume

VEHICLE_VOLUME_S = round(get_volume(VEHICLE_S_WIDTH,VEHICLE_S_HEIGHT,VEHICLE_S_LENGTH), 2)
VEHICLE_VOLUME_M = round(get_volume(VEHICLE_M_WIDTH,VEHICLE_M_HEIGHT,VEHICLE_M_LENGTH), 2)
VEHICLE_VOLUME_L = round(get_volume(VEHICLE_L_WIDTH,VEHICLE_L_HEIGHT,VEHICLE_L_LENGTH), 2)

###
# Calculating distance between different service points
###

# Locations used to calculate distance between service locations
pick_up_location = booking_data['pick_up_location']
drop_off_location = booking_data['drop_off_location']
WM_BASE_LOCATION = '6 St Nicholas Rd, Newbury RG14 5PR, UK'

def distance_matrix(client, origins, destinations,
                    mode=None, language=None, avoid=None, units=None,
                    departure_time=None, arrival_time=None, transit_mode=None,
                    transit_routing_preference=None, traffic_model=None, region=None):

    params = {
        "origins": convert.location_list(origins),
        "destinations": convert.location_list(destinations)
    }

    if mode:
        # NOTE(broady): the mode parameter is not validated by the Maps API
        # server. Check here to prevent silent failures.
        if mode not in ["driving", "walking", "bicycling", "transit"]:
            raise ValueError("Invalid travel mode.")
        params["mode"] = mode

    if language:
        params["language"] = language

    if avoid:
        if avoid not in ["tolls", "highways", "ferries"]:
            raise ValueError("Invalid route restriction.")
        params["avoid"] = avoid

    if units:
        params["units"] = units

    if departure_time:
        params["departure_time"] = convert.time(departure_time)

    if arrival_time:
        params["arrival_time"] = convert.time(arrival_time)

    if departure_time and arrival_time:
        raise ValueError("Should not specify both departure_time and"
                         "arrival_time.")

    if transit_mode:
        params["transit_mode"] = convert.join_list("|", transit_mode)

    if transit_routing_preference:
        params["transit_routing_preference"] = transit_routing_preference

    if traffic_model:
        params["traffic_model"] = traffic_model

    if region:
        params["region"] = region

    return client._request("/maps/api/distancematrix/json", params)

###
# Completing the booking details
###
def complete_booking_details(quote_data, booking_data, items_volume, vehicle_volume_s, vehicle_volume_m, vehicle_volume_l):
    """Function to complete the bookings details after receiving initial user-created details"""
    
    def get_items_volume(booking_data):
        """Function used to get the total volume of the items to be transported"""
        total_volume = 0

        for item in booking_data['serviceCharacteristics']:
            total_volume += items_volume[item] * float(booking_data['serviceCharacteristics'][item])

        return round(total_volume, 2)

    def select_service_vehicle():
        "function used to calculate the most efficient vehicle for the service"
        # Call function to calculate total item's volume
        total_items_volume = get_items_volume(booking_data)

        # Calculate number of trips needed with each vehicle 
        number_of_trips_s_vehicle = ceil(total_items_volume / vehicle_volume_s)
        number_of_trips_m_vehicle = ceil(total_items_volume / vehicle_volume_m)
        number_of_trips_l_vehicle = ceil(total_items_volume / vehicle_volume_l)

        # Determine most efficient vehicle if number of trips is more than 1
        if total_items_volume > vehicle_volume_l:
            if number_of_trips_l_vehicle < number_of_trips_m_vehicle:
                booking_data['vehicle_type'] = 'Large vehicle'
                booking_data['service_cycles'] = number_of_trips_l_vehicle
            elif number_of_trips_m_vehicle <= number_of_trips_s_vehicle:
                booking_data['vehicle_type'] = 'Medium vehicle'
                booking_data['service_cycles'] = number_of_trips_m_vehicle
            elif number_of_trips_s_vehicle <= number_of_trips_m_vehicle and number_of_trips_s_vehicle <= number_of_trips_l_vehicle:
                booking_data['vehicle_type'] = 'Small vehicle'
                booking_data['service_cycles'] = number_of_trips_s_vehicle

        # Determine most efficient vehicle if number of trips is one
        else:
            if total_items_volume < vehicle_volume_s:
                booking_data['vehicle_type'] = 'Small vehicle'
                booking_data['service_cycles'] = number_of_trips_s_vehicle
            elif total_items_volume > vehicle_volume_s and total_items_volume < vehicle_volume_m:
                booking_data['vehicle_type'] = 'Medium vehicle'
                booking_data['service_cycles'] = number_of_trips_m_vehicle
            else:
                booking_data['vehicle_type'] = 'Large vehicle'
                booking_data['service_cycles'] = number_of_trips_l_vehicle

    select_service_vehicle()

    ###
    # Calculating the total distance and time traveled during the service
    ###

    # Places API key and client
    api_key = 'AIzaSyDWCxrQeW0x-4NFupO2fZRoLVA__63S5wQ'
    gmaps = googlemaps.Client(key = api_key)

    # Variables required to call places API function
    pick_up_location = booking_data['pick_up_location']
    drop_off_location = booking_data['drop_off_location']
    service_time = booking_data['service_time']

    # Retrieving all journey details
    journey_base_to_pick_up = distance_matrix(gmaps, WM_BASE_LOCATION, pick_up_location, arrival_time = service_time)
    journey_pick_up_to_drop_off = distance_matrix(gmaps, pick_up_location, drop_off_location)
    journey_drop_off_to_base = distance_matrix(gmaps, drop_off_location, WM_BASE_LOCATION)

    distance_base_to_pick_up = journey_base_to_pick_up['rows'][0]['elements'][0]['distance']['value']
    distance_pick_up_to_drop_off = journey_pick_up_to_drop_off['rows'][0]['elements'][0]['distance']['value']
    distance_drop_off_to_base = journey_drop_off_to_base['rows'][0]['elements'][0]['distance']['value']
    distance_total = (distance_base_to_pick_up + distance_pick_up_to_drop_off + distance_drop_off_to_base) / 1000 # converting m to km
    
    def calculate_price(quote_data, vehicle_type, service_cycles, total_distance):
        
        # Base price based on the KM
        price_per_km = 0.6
        base_price = total_distance * price_per_km
        total_price = 1.00

        # Multiplier depending on vehicle type
        multiplier_small_vehicle = 1
        multiplier_medium_vehicle = 2.00
        multiplier_large_vehicle = 2.50

        if vehicle_type == 'Large vehicle':
            total_price = base_price * multiplier_large_vehicle * service_cycles
            quote_data['amount'] = round(total_price, 2)
        elif vehicle_type == 'Medium vehicle':
            total_price = base_price * multiplier_medium_vehicle * service_cycles
            quote_data['amount'] = round(total_price)
        elif vehicle_type == 'Small vehicle':
            total_price = base_price * multiplier_small_vehicle * service_cycles
            quote_data['amount'] = round(total_price, 2)
        
    calculate_price(quote_data, booking_data['vehicle_type'], booking_data['service_cycles'], distance_total)

