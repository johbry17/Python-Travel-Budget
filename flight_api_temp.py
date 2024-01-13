import requests

def get_flight_cost(api_key, origin, destination, departure_date, return_date=None):
    base_url = "https://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/{country}/{currency}/{locale}/{origin}/{destination}/{outboundDate}"

    params = {
        "apiKey": api_key,
        "country": "US",
        "currency": "USD",
        "locale": "en-US",
        "origin": origin,
        "destination": destination,
        "outboundDate": departure_date,
        "inboundDate": return_date
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Extract flight cost from the response data
        flight_cost = data['Quotes'][0]['MinPrice']
        return flight_cost
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
api_key = f"{NEED_TO_GET}"
flight_cost = get_flight_cost(api_key, "JFK-sky", "LAX-sky", "2024-12-01")
print(f"Estimated flight cost: ${flight_cost}")
