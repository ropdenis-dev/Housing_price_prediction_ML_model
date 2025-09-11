from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('ml-roadmap/', views.ml_roadmap, name='ml_roadmap'),
]