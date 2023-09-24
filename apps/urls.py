from django.urls import path

from apps.views import SignUpView, SignInView, SignInGoogle

urlpatterns = [
    path('sign-up', SignUpView.as_view()),
    path('sign-in', SignInView.as_view()),
    path('oauth2', SignInGoogle.as_view())
]
