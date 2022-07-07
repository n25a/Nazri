from django.urls import path

from views.user import UploadAvatar, SignUp, SignIn, DeleteAvatar

urlpatterns = [
    path("sign-up", SignUp.as_view()),
    path("sign-in", SignIn.as_view()),
    path("apload-avatar", UploadAvatar.as_view()),
    path("delete-avatar", DeleteAvatar.as_view()),
]
