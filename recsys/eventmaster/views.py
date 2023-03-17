from django.shortcuts import get_object_or_404, render
from .models import User, Event

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
            'rated_event': rated_events,
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


