from django.urls import path

from views.user import Users, SignUp, SignIn

urlpatterns = [
    path('sign-up', SignUp.as_view()),
    path('sign-in', SignIn.as_view()),
    path('get-users', Users.as_view()),
]
