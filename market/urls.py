from django.urls import path
from . import views

urlpatterns = [
    path("btc/", views.btc_chart, name="btc_chart"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
