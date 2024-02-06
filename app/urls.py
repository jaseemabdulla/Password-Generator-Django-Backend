from django.urls import path
from .views import GeneratePasswordView,SendPasswordView

urlpatterns = [
    path('generate_password/', GeneratePasswordView.as_view(), name='generate-password'),
    path('send_password_to_email/', SendPasswordView.as_view(), name='send-password-to-email'),
]
