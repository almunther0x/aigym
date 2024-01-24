from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.views.decorators.gzip import gzip_page
from cv2 import *
from .pushup import *
from .dumbbell import *
from .barbell import *


def pushup(request):
    gzip_page
    try:
        cam = PushupCamera(request.user.id)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def dumbbell(request):
    gzip_page
    try:
        cam = DumbbellCamera(request.user.id)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def barbell(request):
    gzip_page
    try:
        cam = BarbellCamera(request.user.id)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def training(request):
    return render(request, 'training.html')

def index(request, *args, **kwargs):
    return render(request, 'index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')