import os

class temperature:
    def __init__(self):
        self.temperature_sensor = os.open("/dev/mlx90614", os.O_RDWR)

    def read_temp(self):
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
        
        return temperature

if __name__ == '__main__':
    temp = temperature()
    print(temp.read_temp())