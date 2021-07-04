from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse
from datetime import datetime
from pi_hardware_info import ModelType, get_info
import sensor.temperature
import json
import camera
import network
import mqtt
import sensor_register
from .models import system_config, sensor_config

'''
Initialize function
'''
# Camera object
cam = camera.mycamera('/dev/video0')

# Network manager object
network_manager = network.wireless()

# Temperature object
temp = sensor.temperature.temperature()

# Sensor register
sensor_table = sensor_register.sensor_register()
sensor_table.register_by_table(temp.register_table())
sensor_table.initial_all_sensor()

# Initialize mqtt
mc = mqtt.mqtt_center()
# Dependence by register table
mc.add_register_table(sensor_table.sensor_table)
mc.run()

'''
Django callback function
'''
# Switch status of mqtt
def mqtt_switch(request):
    # mqtt_config_from_client = json.load(request.body)
    
    # Read mqtt status from database
    current_mqtt_status = system_config.objects.get(name="mqtt")
    
    if current_mqtt_status.value == 'true':
        # Switch status of mqtt 
        current_mqtt_status.value = 'false'
        # turn off mqtt
    else:
        # Switch status of mqtt 
        current_mqtt_status.value = 'true'
        # turn on mqtt


    # Write database
    current_mqtt_status.save()

    return render(request,'html/network.html')

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
    response_data["temperature"] = sensor_table.sensor_table['Temperature']["get_value"]()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def network(request):
    return render(request,'html/network.html')

def network_scan_result(request):
    response_data = {}
    response_data["Network"] = network_manager.scan_network()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def system_time(request):
    response_data = {}
    # Get current time
    now = datetime.now()
    # Convert format
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    response_data["System_time"] = dt_string
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def system_info(request):
    response_data = {}
    info = get_info()
    # Check model
    response_data["Model"] = str(info.model_type)[10:]
    # Check SN
    response_data["SN"] = str(info.serial_number)
    # Check Manufacturer
    response_data["Manufacturer"] = str(info.manufacturer)[13:]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def support_feature(request):
    response_data = {}
    response_data["Support"] = str(["detect, homekit"])
    return HttpResponse(json.dumps(response_data), content_type="application/json")