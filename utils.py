# scheduling, ETA, and notifications

from datetime import datetime, timedelta
from geopy.distance import geodesic

def calculate_eta(current_lat, current_lon, stop_lat, stop_lon, speed_kmh=30):
  distance_km = geodesic((current_lat, current_lon), (stop_lat, stop_lon)).km
  eta_minutes = distance_km / speed_kmh * 60
  return datetime.now() + timedelta(minutes=eta_minutes)