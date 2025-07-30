# Darwix AI Assignment

This repository implements two features for the AI Engineer role screening: 
1. Audio transcription with speaker diarization.
2. AI-generated title suggestions for blog posts.

Built with Django, Whisper (multilingual transcription), pyannote-audio (diarization), and Hugging Face transformers (NLP).

## Setup Instructions
1. Clone the repo: `git clone <your-repo-url>`
2. Create and activate a virtual environment: `python -m venv env` then `source env/bin/activate` (Linux/Mac) or `env\Scripts\activate` (Windows).
3. Install dependencies: `pip install -r requirements.txt`. Note: For pyannote-audio, accept the Hugging Face terms if prompted.
4. Run migrations (if any): `python manage.py migrate`
5. Start the server: `python manage.py runserver`
6. Access at http://localhost:8000/

## Endpoints

### Feature 1: Audio Transcription with Diarization
- **URL:** POST /transcription/transcribe/
- **Input:** Multipart form data with 'audio' key (e.g., WAV file).
- **Output:** JSON structured as {"segments": [{"speaker": "SPEAKER_00", "start": float, "end": float, "text": "transcribed text"}]}
- **Bonus:** Multilingual support via Whisper (auto-detects language).
- **Example Test:** `curl -F audio=@sample.wav http://localhost:8000/transcription/transcribe/`
- **Notes:** Handles multi-speaker audio; output identifies "who spoke when."

### Feature 2: Blog Post Title Suggestions
- **URL:** POST /suggestions/suggest-titles/
- **Input:** Form data with 'content' key (string: blog post text).
- **Output:** JSON as {"titles": ["Suggested Title 1", "Suggested Title 2", "Suggested Title 3"]}
- **Example Test:** `curl -d "content=This is a sample blog post about AI." http://localhost:8000/suggestions/suggest-titles/`
- **Notes:** Uses NLP summarization to generate 3 relevant, concise titles.

## Testing and Evaluation
- **Accuracy:** Test with sample multi-speaker audio (e.g., podcasts) and blog texts.
- **Code Quality:** Modular views, error handling, and temp file management.
- **Robustness:** Handles invalid inputs and exceptions.
- **Dependencies:** Ensure torch is compatible with your system (CPU/GPU).