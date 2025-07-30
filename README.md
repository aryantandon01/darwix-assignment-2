# Darwix AI Assignment

This repository contains the implementation for the AI Engineer role screening assignment at Darwix AI. It includes two main features:
1. **Audio Transcription with Diarization**: Transcribes audio files and identifies speakers (who spoke when), with bonus multilingual support.
2. **AI-Generated Title Suggestions for Blog Posts**: Uses NLP to suggest 3 relevant titles based on blog post content.

The project is built using Django for the web framework, OpenAI Whisper for transcription (multilingual), pyannote-audio for speaker diarization, and Hugging Face transformers/KeyBERT for NLP title generation.

## Prerequisites
- Python 3.11 installed.
- Git for cloning the repository.
- (Optional) A Hugging Face account/token for pyannote-audio (you'll be prompted if needed).
- For audio processing: Install ffmpeg (see notes in Setup Instructions if warnings appear).

## Setup Instructions
Follow these steps in order to get the project running locally:

1. **Clone the Repository**:
   ```
   git clone   # Replace with the actual GitHub URL
   cd aryantandon01-darwix-assignment-2  # Or your repo name
   ```

2. **Create and Activate a Virtual Environment** (recommended to isolate dependencies):
   - On Linux/Mac:
     ```
     python -m venv env
     source env/bin/activate
     ```
   - On Windows:
     ```
     python -m venv env
     env\Scripts\activate
     ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
   - **Note**: If you see a prompt for pyannote-audio, run `huggingface-cli login` and enter your Hugging Face token.
   - **ffmpeg Warning Fix**: If you encounter warnings about ffmpeg during server startup, download and install ffmpeg from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (or gyan.dev for Windows builds). Add its `bin` folder to your system's PATH and restart your terminal.

4. **Apply Migrations** (sets up the default database, though not used in this project):
   ```
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```
   python manage.py runserver
   ```
   - The server will run at http://localhost:8000/ (or http://127.0.0.1:8000/).
   - Press Ctrl+C to stop it.

## Endpoints
The application exposes two API endpoints. Use tools like curl, Postman, or the provided test scripts to interact with them. All responses are in JSON format.

### Feature 1: Audio Transcription with Diarization
- **URL**: POST `/transcription/transcribe/`
- **Input**: Multipart form data with key `'audio'` (upload an audio file, e.g., WAV, MP3, or M4A).
- **Output**: JSON like `{"segments": [{"speaker": "SPEAKER_00", "start": 0.0, "end": 5.0, "text": "Transcribed text"}]}`.
- **Bonus**: Supports multilingual audio (Whisper auto-detects languages).
- **Example Test with curl**:
  ```
  curl -F audio=@path/to/your/sample.wav http://localhost:8000/transcription/transcribe/
  ```
- **Notes**: Ideal for multi-speaker audio (e.g., interviews). Processing time depends on audio length; ensure ffmpeg is installed for non-WAV formats.

### Feature 2: Blog Post Title Suggestions
- **URL**: POST `/suggestions/suggest-titles/`
- **Input**: Form data with key `'content'` (string: the blog post text).
- **Output**: JSON like `{"titles": ["Suggested Title 1", "Suggested Title 2", "Suggested Title 3"]}`.
- **Example Test with curl**:
  ```
  curl -d "content=This is a sample blog post about AI engineering." http://localhost:8000/suggestions/suggest-titles/
  ```
- **Notes**: Uses KeyBERT for keyphrase extraction and T5 for fallbacks, generating concise, relevant titles.

## Testing and Validation
To verify the features:
- **Sample Inputs**: Use multi-speaker audio files (e.g., free podcasts from freesound.org) for transcription and varied blog text for titles.
- **Expected Behavior**: Endpoints return structured JSON; check for accuracy in speaker identification and title relevance.
- **Error Handling**: Invalid requests (e.g., missing audio/content) return JSON errors like `{"error": "Invalid request"}`.
- **Performance Tips**: For faster AI processing, use a GPU if available (torch supports it). Test on CPU first.

### Local Testing Scripts
For quick validation using Python (no need for curl):
- Ensure the server is running (`python manage.py runserver`).
- **Test Title Suggestions**:
  ```
  python test_suggestions.py
  ```
  - Uses sample content; prints status, response, and JSON.
- **Test Transcription**:
  ```
  python test_transcription.py
  ```
  - Update `audio_path` in the script to a valid audio file; prints status, response, and JSON.
- These scripts require the `requests` library (already in requirements.txt).

## Evaluation Notes
- **Code Quality**: Modular structure with error handling and temp file cleanup.
- **Robustness**: Handles edge cases like invalid inputs or short content/audio.
- **Dependencies**: Compatible with CPU/GPU; pin NumPy to 1.26.4 for stability.

If you encounter issues, check server logs for tracebacks or refer to the assignment email for clarifications.