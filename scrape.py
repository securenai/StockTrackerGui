import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://www.cnyes.com/twstock/00919"

# Send an HTTP GET request to the URL
headers = {"User-Agent": "Mozilla/5.0"}  # Add a user-agent to mimic a browser
response = requests.get(url, headers=headers)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Example: Extract Stock Title (e.g., name/code)
stock_title = soup.find("h2", class_="jsx-2312976322").text  # Update the class based on the website

# Example: Extract Stock Data (update the selectors accordingly)
price = soup.find("h3", class_="jsx-2312976322").text  # Inspect element to find appropriate tag/class

# Print the extracted data
print("Stock:", stock_title)
print("Price:", price)

# You can add more extractions based on the page structure
