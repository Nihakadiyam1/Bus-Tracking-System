from django.db import models
from django.contrib.auth.models import User

class Bus(models.Model):
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey('Route', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.number} - {self.name}"

class Stop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=100)
    stops = models.ManyToManyField(Stop, through='RouteStop')

    def __str__(self):
        return self.name

class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()
    scheduled_arrival = models.TimeField()
    scheduled_departure = models.TimeField()

    class Meta:
        ordering = ['sequence']

class LocationUpdate(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delayed = models.BooleanField(default=False)
    eta_to_next_stop = models.DateTimeField(null=True, blank=True)
