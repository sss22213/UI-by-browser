from apps.models import sensor_config, mqtt_config
import paho.mqtt.client as mqtt
import threading
import datetime 
import json
import time

# All transfer sent by json 
class mqtt_center:
    # Func array store all of function
    def __init__(self):
        self.client = mqtt.Client()

        # Create threading
        self.mqtt_thread = threading.Thread(target = self.publish_topic)

        # Create state flag
        self.flag = 1

        # 
        self.config_connect_info()

    def add_register_table(self, register_table):
        self.register_table = register_table

    def config_connect_info(self):
        mqtt_info = mqtt_config.objects.get(id=1)
        self.mqtt_url = mqtt_info.url.strip()
        self.mqtt_port = mqtt_info.port
        self.mqtt_user = None
        self.mqtt_pwd = None

    def connect_server(self):
        # Config login in username and password
        if (self.mqtt_user is not None) and (self.mqtt_pwd is not None):
            self.client.username_pw_set(self.mqtt_user, self.mqtt_pwd)
        # Connect to mqtt server
        self.client.connect(self.mqtt_url, self.mqtt_port, 60)

    def publish_topic(self):
        #  Connect server
        self.connect_server()
        # Publish all of topic
        while True:
            if self.flag:
                sensor_info = sensor_config.objects.all()
                for key in sensor_info:
                    name = key.name
                    get_value = self.register_table[name]["get_value"]
                    status = key.mqtt_status

                    if status:
                        value_to_dic = {"value": get_value()}
                        self.client.publish(name, json.dumps(value_to_dic))
                        time.sleep(0.01)
            else:
                self.client.disconnect()
                break

    def run(self):
        self.flag = 1

        # Create threading
        self.mqtt_thread = threading.Thread(target = self.publish_topic)
        self.mqtt_thread.start()


    def stop(self):
        self.flag = 0

if __name__ == '__main__':
    1 == 1

