from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from keybert import KeyBERT  # New import for keyphrase extraction
from transformers import pipeline  # Kept for fallback summarization

@csrf_exempt
def suggest_titles(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if not content:
            return JsonResponse({"error": "Content required"}, status=400)
        
        try:
            # Primary method: Use KeyBERT for keyphrase-based titles
            kw_model = KeyBERT()  # Defaults to 'distilbert-base-nli-mean-tokens' embedding model
            keywords = kw_model.extract_keywords(
                content,
                keyphrase_ngram_range=(1, 3),  # Allow 1-3 word phrases for title-like suggestions
                stop_words='english',          # Remove common words
                top_n=3,                       # Get top 3 keyphrases
                diversity=0.5                  # Ensure some variety in suggestions
            )
            
            # Format keyphrases as titles (capitalize and clean)
            titles = [phrase.title().strip() for phrase, _ in keywords]
            
            # If fewer than 3, fallback to summarization for additional suggestions
            if len(titles) < 3:
                generator = pipeline('summarization', model='t5-small')
                prompt = f"Generate a concise blog title for: {content}"
                summaries = generator(prompt, max_length=15, num_return_sequences=3 - len(titles), do_sample=True)
                additional_titles = [summary['summary_text'].title().strip().rstrip('.') for summary in summaries]
                titles.extend(additional_titles)
            
            # Ensure exactly 3 unique titles
            unique_titles = list(set(titles))[:3]
            if len(unique_titles) < 3:
                unique_titles.extend(["Generated Title Suggestion"] * (3 - len(unique_titles)))
            
            return JsonResponse({"titles": unique_titles})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request: POST with 'content' required"}, status=400)
