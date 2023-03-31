from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UsersView, BusinessesView, UserDetailView, BusinessDetailView
from .import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(next_page='/reviewmaster/businesses',
                                                template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=None,
                                                  template_name='registration/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(template_name='registration/register.html'), name='register'),
    # path('users/', views.user_index, name="user_index"),
    path('users/', UsersView.as_view(template_name='reviewmaster/user_index.html'), name="user_index"),
    # path('users/<str:user_id>', views.user_detail, name="user_detail"),
    path('users/<str:pk>', UserDetailView.as_view(template_name='reviewmaster/user_detail.html'), \
         name="user_detail"),
    # path('businesses/', views.business_index, name="business_index"),
    path('businesses/', BusinessesView.as_view(template_name='reviewmaster/business_index.html')),
    # path('businesses/<str:business_id>', views.business_detail, name="business_detail"),
    path('businesses/<str:pk>', BusinessDetailView.as_view(template_name="reviewmaster/business_detail.html"), \
         name="business_detail"),
    path('demo/yelp-businesses', views.demo_yelp_businesses),
    path('demo/yelp-business-reviews/<slug:business_id>', views.demo_yelp_business_reviews),
    path('demo/yelp-dump-data', views.dump_yelp_data),

]
