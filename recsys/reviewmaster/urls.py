from django.urls import path
from .import views

urlpatterns = [
    path('users/', views.user_index),
    path('users/<int:user_id>', views.user_detail),
    path('businesses/', views.business_index),
    path('businesses/<int:business_id>', views.business_detail),
    path('demo/yelp-businesses', views.demo_yelp_businesses),
    path('demo/yelp-business-reviews/<slug:business_id>', views.demo_yelp_business_reviews),
]
