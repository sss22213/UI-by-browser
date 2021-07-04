from apps.models import sensor_config

class sensor_register:
    def __init__(self):
        self.sensor_table = {}
    
    def register(self, sensor_name, initial_func, get_value_func, deinitializes_func):
        sensor_in_database = False

        # Check sensor name is exist at database
        for sensor_info in sensor_config.objects.all():
            if sensor_info.name == sensor_name:
                sensor_in_database = True
        if sensor_in_database == False:
            print('Failed to register {}'.format(sensor_name))
            return

        self.sensor_table[sensor_name] = {}
        self.sensor_table[sensor_name]["initial"] = initial_func
        self.sensor_table[sensor_name]["get_value"] = get_value_func
        self.sensor_table[sensor_name]["deinitializes"] = deinitializes_func
        
    def initial_all_sensor(self):
        # Initialize all of sensor
        for key in self.sensor_table:
            self.sensor_table[key]["initial"]()

    def register_by_table(self, register_table):
        name = register_table["sensor_name"]
        self.sensor_table[name] = {}
        self.sensor_table[name]["initial"] = register_table['initial']
        self.sensor_table[name]["get_value"] = register_table['get_value']
        self.sensor_table[name]["deinitializes"] = register_table['deinitializes']

