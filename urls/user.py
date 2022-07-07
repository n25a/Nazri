from django.urls import path

from views.user import SignUp, SignIn

urlpatterns = [
    path("sign-up", SignUp.as_view()),
    path("sign-in", SignIn.as_view()),
]
