from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import User, Event
from django.conf import settings
import requests


# Create your views here.


def user_index(request):
    users = User.objects.all()
    return render(request, 'eventmaster/user_index.html', {'users': users})


def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    rated_events = user.rated_events()
    content_based_recommended_events = user.content_based_recommended_events()
    collaborative_based_recommended_events = user.collaborative_based_recommended_events()

    return render(
        request,
        'eventmaster/user_detail.html',
        {
            'user': user,
            'rated_events': rated_events,
            'content_based_recommended_events': content_based_recommended_events,
            'collaborative_based_recommended_events': collaborative_based_recommended_events
        }
    )


def event_index(request):
    events = Event.objects.all()
    return render(request, 'eventmaster/event_index.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'eventmaster/event_detail.html', {'event': event})


def demo_yelp_businesses(request):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': 'Bearer ' + settings.YELP_API_KEY
    }
    params = {
        'location': 'Bay Area',
        'limit': 50
    }
    # Send the request to the Yelp Fusion API
    response = requests.get(url, headers=headers, params=params)
    return JsonResponse(response.json(), json_dumps_params={'indent': 4}, safe=False)


def demo_yelp_business_reviews(request, business_id):
    url = f'https://api.yelp.com/v3/businesses/{business_id}/reviews'
    headers = {
        'Authorization': 'Bearer ' + settings.YELP_API_KEY
    }
    params = {
        'limit': 10
    }
    # Send the request to the Yelp Fusion API
    response = requests.get(url, headers=headers, params=params)
    return JsonResponse(response.json(), json_dumps_params={'indent': 4}, safe=False)
