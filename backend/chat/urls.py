from django.urls import path
from .views import SendMessageAPIView

urlpatterns = [
    path('send', SendMessageAPIView.as_view(), name='send_message'),
]
