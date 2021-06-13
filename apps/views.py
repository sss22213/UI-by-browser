from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse
import temperature
import json
import camera
import network

# camera object
cam = camera.mycamera('/dev/video0')

# temperature object
temp = temperature.temperature()

# network manager object
network_manager = network.wireless()

# Create your views here.
def homepage(request):
    return render(request,'html/index.html')

@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(camera.gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def detect(request):
    return render(request,'html/detect.html')

def read_temperature(request):
    response_data = {}
    response_data["temperature"] = temp.read_temp()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def network(request):
    return render(request,'html/network.html')

def network_scan_result(request):
    response_data = {}
    response_data["Network"] = network_manager.scan_network()
    return HttpResponse(json.dumps(response_data), content_type="application/json")