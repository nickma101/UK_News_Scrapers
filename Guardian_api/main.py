import requests

# Set up API endpoint and query parameters
endpoint = "https://content.guardianapis.com/search"
params = {
    "api-key": 4ed35a9f-ee74-47db-8cc6-0aac0a181417
}

query_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={apikey}"

# Send GET request to API endpoint
response = requests.get(endpoint, params=params)

# Check if request was successful
if response.status_code != 200:
    print("Error:", response.status_code)
else:
    # Parse JSON response into Python dictionary
    data = response.json()

    # Loop through each article and print its title and URL
    for article in data["response"]["results"]:
        print(article["webTitle"])
        print(article["webUrl"])