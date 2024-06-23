import requests

# Define the URL for the POST request
url = "http://127.0.0.1:8000/sum"

# Define the payload with the numbers to be summed
data = {
    "number1": 5,
    "number2": 7
}

# Send the POST request
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()
    print("Response:", response.json())
else:
    #print(f"Failed to get a valid response. Status code: {response.status_code}")
    print(f"Error: {response.text}")
