import os
import tempfile
from django.http import JsonResponse
import whisper
from pyannote.audio import Pipeline
from pydub import AudioSegment  # For potential audio conversion
from django.views.decorators.csrf import csrf_exempt  # Add this

@csrf_exempt  # Add this

def transcribe_audio(request):
    if request.method == 'POST' and 'audio' in request.FILES:
        audio_file = request.FILES['audio']
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            audio_path = tmp_file.name
        
        try:
            # Load models
            model = whisper.load_model("base")  # Use "large" for better multilingual support
            transcription = model.transcribe(audio_path, fp16=False)  # Multilingual via auto-detect
            
            pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=True)
            diarization = pipeline(audio_path)
            
            # Simplified merging: Align transcription segments with diarization turns
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                # Find matching transcription text by timestamp overlap (approximate)
                matching_text = next((seg['text'] for seg in transcription['segments'] 
                                      if seg['start'] < turn.end and seg['end'] > turn.start), "Unknown")
                segments.append({
                    "speaker": speaker,
                    "start": turn.start,
                    "end": turn.end,
                    "text": matching_text.strip()
                })
            
            # Clean up temp file
            os.unlink(audio_path)
            
            return JsonResponse({"segments": segments})
        except Exception as e:
            os.unlink(audio_path)  # Cleanup on error
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request: POST with 'audio' file required"}, status=400)
