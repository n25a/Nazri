from django.urls import path

from views.reason import GetReasons, DeleteReason, AddReason

urlpatterns = [
    path('add', AddReason.as_view()),
    path('get', GetReasons.as_view()),
    path('delete', DeleteReason.as_view()),
]
