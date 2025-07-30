from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transcription/', include('transcription.urls')),
    path('suggestions/', include('suggestions.urls')),
]
