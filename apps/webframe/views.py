from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import photos
import os, sys
import json

def homepage(request):
    return render(request, 'webframe/homepage.html')

def image(request):
    images = photos.objects.last()
    context = {
        'images' : images
    }
    return render(request, 'webframe/image.html', context)

def webcam(request):
    return render(request, 'webframe/webcam.html')

def upload(request):
    image = request.FILES['img']
    photos.objects.create(img = image)
    return redirect('/ml_image')

def ml_image(request):
    pic = photos.objects.last()
    context = {
        'images' : pic
    }
    return render(request, 'webframe/ml_image.html', context)


