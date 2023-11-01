import requests
from bs4 import BeautifulSoup
import re
import json

# The URL of the webpage you want to scrape
url = "https://www.bee-link.com/computer-73493777"

# Send an HTTP request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'lxml')

    # Find the script tags
    script_tags = soup.find_all("script")

    # Initialize an empty variable to hold the 'data' JSON
    data_json = None

    # Loop through the script tags to find the 'data' variable
    for script in script_tags:
        script_content = script.string
        if script_content:
            data_match = re.search(r'data\s*=\s*({.*?});', script_content, re.DOTALL)
            if data_match:
                data_json = data_match.group(1)
                break  # Stop when the 'data' variable is found

    if data_json:
        # Parse the 'data' variable as a JSON object
        data_object = json.loads(data_json)

        # Check if the 'products' key exists in the 'data' JSON
        if 'products' in data_object:
            products = data_object['products']
            for product in products:
                print(product['title'])
                configurations = product['configurations']
                for config in configurations:
                    print("	Ram:", config['RAM'], ", Storage:", config['Storage'], ", Price:", config['price'])
        else:
            print("'products' key not found in the 'data' JSON.")
    else:
        print("Data variable not found in the JavaScript code.")

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
