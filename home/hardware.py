# your_app/views.py

import requests
import json
from django.http import JsonResponse
import django
django.setup()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")


def fetch_thingspeak_data(num_entries=1):
    base_url = 'https://api.thingspeak.com/channels/2375718/feeds.json?api_key=ATHYX1B78TCPT7W6&results=2'
    params = {'results': num_entries}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Write data to JSON file
        json_filename = 'thingspeak_data.json'
        with open(json_filename, mode='w') as json_file:
            json.dump(data, json_file, indent=2)

        return {'success': f'Data written to {json_filename}'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def your_view():
    # Replace 'YOUR_API_KEY' and 'YOUR_CHANNEL_ID' with your actual ThingSpeak API key and channel I

    result = fetch_thingspeak_data()

    # Process result and return a JSON response
    return JsonResponse(result)

your_view()
