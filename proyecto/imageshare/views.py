import requests
from django.shortcuts import render, redirect
from .form import ImageForm
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def image_upload_view(request):
    pictshare_url = None
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_file = request.FILES['image']
            
            # Subir la imagen a Pictshare
            files = {'file': image_file}
            response = requests.post('http://localhost:9080/api/upload.php', files=files)

            print(f"Respuesta de Pictshare: {response.text}")

            if response.status_code == 200:
                pictshare_url = response.json().get('url', None)
                if pictshare_url:
                    image_instance.pictshare_url = pictshare_url
                    image_instance.save()

                return render(request, 'upload.html', {'form': form, 'pictshare_url': pictshare_url})
            else:
                form.add_error(None, 'Error al subir la imagen a Pictshare')
    else:
        form = ImageForm()
    
    return render(request, 'upload.html', {'form': form, 'pictshare_url': pictshare_url})