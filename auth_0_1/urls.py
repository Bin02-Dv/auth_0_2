from django.urls import path
from .views import SignUpView, LoginView, UserView, LogoutView, AllUserView, GenerateAPIKeyView

urlpatterns = [
    path('api-keys/', GenerateAPIKeyView.as_view(), name='generate_api_key'),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user', UserView.as_view()),
    path('', AllUserView.as_view()),
]