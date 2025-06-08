from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('loggedin/', views.loggedin_page, name='loggedin'),
    path('itinerary/', views.itinerary_page, name='itinerary'),
    path('chat/', views.chatbot_view, name='chatbot'),
]
