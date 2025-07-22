from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bus, Stop, Route, RouteStop, LocationUpdate

class BusModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='driver1', password='testpass')
        self.bus = Bus.objects.create(number='101', name='Main Street', driver=self.user)

    def test_bus_creation(self):
        self.assertEqual(self.bus.number, '101')
        self.assertEqual(str(self.bus), '101 - Main Street')

class StopModelTest(TestCase):
    def test_stop_creation(self):
        stop = Stop.objects.create(name='Central', latitude=28.6, longitude=77.2)
        self.assertEqual(str(stop), 'Central')

class RouteModelTest(TestCase):
    def setUp(self):
        self.route = Route.objects.create(name='Route 1')
        self.stop1 = Stop.objects.create(name='A', latitude=0, longitude=0)
        self.stop2 = Stop.objects.create(name='B', latitude=1, longitude=1)
        RouteStop.objects.create(route=self.route, stop=self.stop1, sequence=1, scheduled_arrival='08:00', scheduled_departure='08:05')
        RouteStop.objects.create(route=self.route, stop=self.stop2, sequence=2, scheduled_arrival='08:30', scheduled_departure='08:35')

    def test_route_stops_order(self):
        stops = list(self.route.stops.order_by('routestop__sequence'))
        self.assertEqual(stops[0].name, 'A')
        self.assertEqual(stops[1].name, 'B')

class LocationUpdateTest(TestCase):
    def setUp(self):
        self.bus = Bus.objects.create(number='202', name='Downtown')
        self.update = LocationUpdate.objects.create(bus=self.bus, latitude=12.34, longitude=56.78)

    def test_location_update_creation(self):
        self.assertEqual(self.update.bus.number, '202')
        self.assertAlmostEqual(self.update.latitude, 12.34)
