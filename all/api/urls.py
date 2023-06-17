from django.urls import path
from all.api.views import *

urlpatterns = [
    path('create-loan/', LoanCreate.as_view()),
    path('create-reservation/', ReservationCreate.as_view()),
    path('create-review/', ReviewCreate.as_view()),
    path('create-favorite/', FavoriteCreate.as_view()),
]
