from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import User, Business
from django.conf import settings
import requests


# Create your views here.


def user_index(request):
    users = User.objects.all()
    return render(request, 'reviewmaster/user_index.html', {'users': users})


def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    rated_businesses = user.rated_businesses()
    content_based_recommended_businesses = user.content_based_recommended_businesses()
    collaborative_based_recommended_businesses = user.collaborative_based_recommended_businesses()

    return render(
        request,
        'reviewmaster/user_detail.html',
        {
            'user': user,
            'rated_businesses': rated_businesses,
            'content_based_recommended_businesses': content_based_recommended_businesses,
            'collaborative_based_recommended_businesses': collaborative_based_recommended_businesses
        }
    )


def business_index(request):
    businesses = Business.objects.all()
    return render(request, 'reviewmaster/business_index.html', {'businesses': businesses})


def business_detail(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    return render(request, 'reviewmaster/business_detail.html', {'business': business})


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
