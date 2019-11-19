from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import photos
import json as simplejson

def homepage(request):
    return render(request, 'webframe/homepage.html')

def image(request):
    images = photos.objects.first()
    context = {
        'images' : images
    }
    return render(request, 'webframe/image.html', context)

def webcam(request):
    return render(request, 'webframe/webcam.html')

def upload(request):
    image = request.POST['img']
    photos.objects.create(img = image)
        
    return redirect('upload')
