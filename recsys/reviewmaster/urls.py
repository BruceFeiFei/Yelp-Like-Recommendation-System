from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(next_page='/reviewmaster/businesses',
                                                template_name='registration/login.html'), name='login'),
    path('register/', views.RegisterView.as_view(template_name='registration/register.html'), name='register'),
    path('users/', views.user_index, name="user_detail"),
    path('users/<str:user_id>', views.user_detail, name="user_detail"),
    path('businesses/', views.business_index, name="business_index"),
    path('businesses/<str:business_id>', views.business_detail, name="business_detail"),
    path('demo/yelp-businesses', views.demo_yelp_businesses),
    path('demo/yelp-business-reviews/<slug:business_id>', views.demo_yelp_business_reviews),
    path('demo/yelp-dump-data', views.dump_yelp_data),

]
