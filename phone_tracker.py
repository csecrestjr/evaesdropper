import sqlite3
import phonenumbers
from phonenumbers import geocoder
from geopy.geocoders import Nominatim

# Connect to the database
conn = sqlite3.connect("phone_numbers.db")
cursor = conn.cursor()

# Create the phone_numbers table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS phone_numbers (
        id INTEGER PRIMARY KEY,
        number TEXT,
        location TEXT
    )
""")

# Function to get more precise address of a region
def get_address_from_region(region):
    geolocator = Nominatim(user_agent="phone_tracker_app")
    location = geolocator.geocode(region)
    return location.address if location else "Address not found"

# Function to get region of a phone number
def get_phone_number_region(number):
    try:
        phone_number = phonenumbers.parse(number)
        return geocoder.description_for_number(phone_number, 'en')
    except phonenumbers.phonenumberutil.NumberParseException:
        return "Invalid number"

# Function to track any phone number
def track_phone_number(number):
    try:
        # Retrieve the region of the phone number
        region = get_phone_number_region(number)
        # Get more precise address of the region
        location_str = get_address_from_region(region)

        # Insert the phone number and its location into the database
        cursor.execute("INSERT INTO phone_numbers (number, location) VALUES (?, ?)",
                       (number, location_str))
        conn.commit()
        print("Phone number tracked successfully.")
    except sqlite3.Error as e:
        print(f"Error tracking phone number: {e}")

# Example usage of track_phone_number function
phone_number = input("Enter a phone number to track: ")
track_phone_number(phone_number)

# Function to retrieve tracked phone numbers
def retrieve_phone_numbers():
    try:
        # Retrieve all phone numbers and their locations from the database
        cursor.execute("SELECT * FROM phone_numbers")
        rows = cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                print(f"Number: {row[1]}, Location: {row[2]}")
        else:
            print("No phone numbers tracked.")
    except sqlite3.Error as e:
        print(f"Error retrieving phone numbers: {e}")

# Example usage of retrieve_phone_numbers function
retrieve_phone_numbers()

# Close the database connection
conn.close()
