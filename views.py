from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import Bus, LocationUpdate, Stop
from .forms import UserRegisterForm
import json

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def buses_api(request):
    bus_number = request.GET.get('bus_number')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    buses = Bus.objects.all()
    if bus_number:
        buses = buses.filter(number__icontains=bus_number)
    # For source/destination filtering, you can expand this logic as needed.
    result = []
    for bus in buses:
        latest = LocationUpdate.objects.filter(bus=bus).order_by('-timestamp').first()
        result.append({
            'number': bus.number,
            'name': bus.name,
            'is_delayed': latest.is_delayed if latest else False,
            'eta': latest.eta_to_next_stop.strftime('%H:%M') if latest and latest.eta_to_next_stop else None,
            'latitude': latest.latitude if latest else None,
            'longitude': latest.longitude if latest else None,
        })
    return JsonResponse(result, safe=False)

@csrf_exempt
def esp32_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bus_number = data['bus_number']
            latitude = data['latitude']
            longitude = data['longitude']
            timestamp = timezone.now()
            bus = Bus.objects.get(number=bus_number)
            LocationUpdate.objects.create(
                bus=bus,
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp
            )
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'bus_{bus_number}',
                {
                    'type': 'send_location',
                    'data': {
                        'latitude': latitude,
                        'longitude': longitude,
                        'timestamp': str(timestamp),
                    }
                }
            )
            return JsonResponse({'Status': 'success'})
        except Exception as e:
            return JsonResponse({'Status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'Status': 'error', 'message': 'Invalid request'}, status=400)
