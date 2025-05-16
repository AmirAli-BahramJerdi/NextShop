from django.urls import path
from .views import HomeView, NewsletterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
]