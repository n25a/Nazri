from django.urls import path

from views.penalty import PenaltyView, Pay, NazriGiver, GetPenalties

urlpatterns = [
    path('add', PenaltyView.as_view()),
    path('get', GetPenalties.as_view()),
    path('nazri-givers', NazriGiver.as_view()),
    path('pay', Pay.as_view()),
]
