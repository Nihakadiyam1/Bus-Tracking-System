from django.contrib import admin
from .models import Bus, Stop, Route, RouteStop, LocationUpdate

class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'driver', 'route')
    search_fields = ('number', 'name')

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [RouteStopInline]
    # filter_horizontal = ('stops',)

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'stop', 'sequence', 'scheduled_arrival', 'scheduled_departure')
    list_filter = ('route',)

@admin.register(LocationUpdate)
class LocationUpdateAdmin(admin.ModelAdmin):
    list_display = ('bus', 'latitude', 'longitude', 'timestamp', 'is_delayed', 'eta_to_next_stop')
    list_filter = ('bus', 'is_delayed')
    search_fields = ('bus__number',)
