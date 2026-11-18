from django.urls import path

from .views import LoginView, EmailCheckView

urlpatterns=[
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]