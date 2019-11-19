from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import photos

def homepage(request):
    return render(request, 'webframe/homepage.html')

def image(request):
    images = photos.objects.last()
    context = {
        'images' : images.img
    }
    return render(request, 'webframe/image.html', context)

def webcam(request):
    return render(request, 'webframe/webcam.html')

def upload(request):
    image = request.POST['img']
    photos.objects.create(img = image)
    print('TESTING')
    return redirect('/images')
