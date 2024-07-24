import requests
echo "##active_line2##"

echo "##active_line3##"
# URL of the API
echo "##active_line4##"
url = https://jsonplaceholder.typicode.com/posts
echo "##active_line5##"

echo "##active_line6##"
# Send a GET request to fetch the data
echo "##active_line7##"
response = requests.get(url)
echo "##active_line8##"

echo "##active_line9##"
# Save the response data to api_data.json
echo "##active_line10##"
with open(api_data.json, w) as file:
echo "##active_line11##"
    file.write(response.text)
echo "##active_line12##"

