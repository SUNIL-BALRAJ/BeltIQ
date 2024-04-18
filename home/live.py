import json
import requests
import os
while True:
    base_url = ''
    params = {'results': 1}
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json() 


    # Write the updated data back to the file
    with open(r'C:\Users\sumit\OneDrive\Desktop\BeltIQ\static\assets\thingspeaks_data.json','w') as file:
        json.dump(data, file, indent=2)