from django.urls import path
from .import views

urlpatterns = [
    path('users/', views.user_index),
    path('users/<int:user_id>', views.user_detail),
    path('events/', views.event_index),
    path('events/<int:event_id>',views.event_detail),
]