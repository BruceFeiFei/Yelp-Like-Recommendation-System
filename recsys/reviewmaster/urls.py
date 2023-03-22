from django.urls import path
from .import views

urlpatterns = [
    path('users/', views.user_index, name="user_detail"),
    path('users/<str:user_id>', views.user_detail, name="user_detail"),
    path('businesses/', views.business_index, name="business_index"),
    path('businesses/<str:business_id>', views.business_detail, name="business_detail"),
    path('demo/yelp-businesses', views.demo_yelp_businesses),
    path('demo/yelp-business-reviews/<slug:business_id>', views.demo_yelp_business_reviews),
    path('demo/yelp-dump-data', views.dump_yelp_data),
]
