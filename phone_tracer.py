import json
import requests

def get_phone_location(phone_number, api_key):
    url = f'https://maps.googleapis.com/maps/api/geolocation/v1/geolocate?key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()
        latitude = data['latitude']
        longitude = data['longitude']
        return latitude, longitude
    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", e)
        return None, None
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        return None, None

def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="phone_tracker")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    return location.address
    pass

def track_phone():
    phone_number = input("Enter phone number: ")
    api_key = input("Enter your API key: ")
    latitude, longitude = get_phone_location(phone_number, api_key)
    if latitude is not None and longitude is not None:
        address = get_address(latitude, longitude)
        print("Address:", address)

def main():
    track_phone()

if __name__ == "__main__":
    main()
