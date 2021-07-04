import os
import time

class temperature:
    def __init__(self):
        self.sensor_name = "Temperature"

    def initialize(self):
        # Open device of measure temperature
        self.temperature_sensor = os.open("/dev/mlx90614", os.O_RDWR)

    def deinitialize(self):
        os.close("/dev/mlx90614")

    # Read temperature from sensor
    def get_value(self):
        # For save temperature
        temperature = {}

        # Read temperature from snesor
        temp = os.read(self.temperature_sensor, 3)

        # TA
        temperature["TA"] = str(round((temp[0] | temp[1] << 8) * 0.02 - 273.15, 2))

        # TOBJ1(Include calibrate)
        temperature["TOBJ1"] = str(round((temp[2] | temp[3] << 8) * 0.02 - 273.15 + 1, 2))

        # TOBJ2
        temperature["TOBJ2"] = str(round((temp[4] | temp[5] << 8) * 0.02 - 273.15, 2))

        time.sleep(0.5)

        return temperature

    # Register table
    def register_table(self):
        sensor_message = {}
        sensor_message["sensor_name"] = self.sensor_name
        sensor_message["initial"] = self.initialize
        sensor_message["get_value"] = self.get_value
        sensor_message["deinitializes"] = self.deinitialize
        return sensor_message


if __name__ == '__main__':
    temp = temperature()
    temp.run()
    while True:
        print(temp.read_temp())
        time.sleep(1)