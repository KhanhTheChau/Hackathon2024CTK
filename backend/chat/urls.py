from django.urls import path
from .views import SendMessageAPIView

urlpatterns = [
    path('api/v1/messages/send', SendMessageAPIView.as_view(), name='send_message'),
]
