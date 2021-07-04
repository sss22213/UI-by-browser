from django.db import models

# System config
class system_config(models.Model):
    name = models.CharField(
        max_length = 100
    )

    value = models.CharField(
        max_length = 100
    )

class sensor_config(models.Model):
    name = models.CharField(
        max_length = 100
    )

    mqtt_status = models.IntegerField()

class mqtt_config(models.Model):
    url = models.CharField(
        max_length = 20
    )

    username = models.CharField(
        max_length = 100
    )

    password = models.CharField(
        max_length = 100
    )

    port = models.IntegerField()

    support = models.CharField(
        max_length = 500
    )

