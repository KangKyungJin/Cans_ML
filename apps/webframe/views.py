from django.shortcuts import render, redirect

def homepage(request):
    return render(request, 'webframe/homepage.html')

def images(request):
    return render(request, 'webframe/image.html')

def webcam(request):
    return render(request, 'webframe/webcam.html')
