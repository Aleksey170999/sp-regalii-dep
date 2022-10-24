from django.urls import path
from .views import genreg

urlpatterns = [
    path('regals/', genreg),
]
