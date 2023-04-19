from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import User, Business, Review
from django.conf import settings
import requests


# Create your views here.

@staff_member_required
def user_index(request):
    users = User.objects.all()
    return render(request, 'reviewmaster/user_index.html', {'users': users})


@login_required
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


def dump_yelp_data(request):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': 'Bearer ' + settings.YELP_API_KEY
    }
    params = {
        'location': 'Bay Area',
        'limit': 50
    }
    business_count = 0
    review_count = 0
    actual_user_count = 0
    fake_user_count = 0
    # Send the request to the Yelp Fusion API
    response = requests.get(url, headers=headers, params=params)
    for business_data in response.json()['businesses']:
        # Create a new Business object and save it to the database
        business = Business(
            id=str(business_data['id']),
            alias=business_data['alias'],
            name=business_data['name'],
            image_url=business_data['image_url'],
            is_closed=business_data['is_closed'],
            url=business_data['url'],
            review_count=business_data['review_count'],
            rating=business_data['rating'],
            latitude=business_data['coordinates']['latitude'],
            longitude=business_data['coordinates']['longitude'],
            price=business_data.get('price', '$'),
            city=business_data['location']['city'],
            zip_code=business_data['location']['zip_code'],
            country=business_data['location']['country'],
            state=business_data['location']['state'],
            address=' '.join(business_data['location']['display_address']),
            phone=business_data['phone'],
        )
        business.save()
        business_count += 1

        # Make a separate API request to get the reviews for this business
        review_url = f'https://api.yelp.com/v3/businesses/{business_data["id"]}/reviews'
        review_params = {
            'limit': 10
        }
        review_response = requests.get(review_url, headers=headers, params=review_params)
        for review_data in review_response.json()['reviews']:
            # Update or create a user if not exist
            # (Considering the sparsity of user data, retain only the first alphanumeric characters of
            # the user id. In total, a max of 26*2+10 users will be saved)
            fake_id = review_data['user']['id'][0]
            fake_email = fake_id + '@gmail.com'
            user, created = User.objects.update_or_create(
                id=fake_id,
                defaults={
                    'profile_url': review_data['user']['profile_url'],
                    'image_url': review_data['user']['image_url'],
                    'name': review_data['user']['name'],
                    'username': fake_id,
                    # 'email': fake_id + '@gamil.com',
                    'email': fake_email,
                },
            )
            actual_user_count += 1
            if created:
                fake_user_count += 1
            review = Review(
                id=review_data['id'],
                url=review_data['url'],
                text=review_data['text'],
                rating=review_data['rating'],
                time_created=review_data['time_created'],
                user=user,
                business=business,
            )
            review.save()
            review_count += 1

    return JsonResponse(
        data={
            'business_count': business_count,
            'review_count': review_count,
            'actual_user_count': actual_user_count,
            'fake_user_count': fake_user_count,
        }
    )


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('user_detail', user_id=username)
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # models.User
        fields = ('email', 'username', 'id', 'name', 'password1', 'password2')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # redirect to log_in if success


class UsersView(ListView):
    model = User
    template_name = 'reviewmaster/user_index.html'


class UserDetailView(DetailView):
    model = User
    template_name = 'reviewmaster/user_detail.html'

    # override context data
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["rated_businesses"] = user.rated_businesses()
        context["content_based_recommended_businesses"] = user.content_based_recommended_businesses()
        context["collaborative_based_recommended_businesses"] = user.collaborative_based_recommended_businesses()
        return context


class BusinessesView(ListView):
    model = Business
    template_name = 'reviewmaster/business_index.html'


class BusinessDetailView(DetailView):
    model = Business

