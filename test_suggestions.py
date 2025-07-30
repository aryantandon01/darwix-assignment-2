import requests

url = "http://127.0.0.1:8000/suggestions/suggest-titles/"
data = {"content": "This is a blog post about AI engineering and Django."}

response = requests.post(url, data=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # This shows the raw output

# Only try JSON if status is 200
if response.status_code == 200:
    try:
        print("JSON Response:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse JSON - response is not valid JSON.")
else:
    print("Non-200 status - check server logs for errors.")
