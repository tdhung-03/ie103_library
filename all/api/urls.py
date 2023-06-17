from django.urls import path
from all.api.views import *

urlpatterns = [
    path('create-loan/', LoanCreate.as_view())
]
