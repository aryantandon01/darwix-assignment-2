import requests

# Replace with the path to your actual sample audio file (e.g., 'D:\\path\\to\\sample.wav')
audio_path = 'D:\\GitHubProjects\\darwix-assignment-2\\videoplayback.m4a'  # Must be a valid file!

url = "http://127.0.0.1:8000/transcription/transcribe/"

# Open the file in binary mode for upload
try:
    with open(audio_path, 'rb') as audio_file:
        files = {'audio': audio_file}
        response = requests.post(url, files=files)
except FileNotFoundError:
    print(f"Error: Audio file not found at {audio_path}. Please update the path and try again.")
    exit(1)  # Stop script if file missing

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
