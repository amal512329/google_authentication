from django.urls import path
from app.views import IndexViews

urlpatterns = [
    path('',IndexViews.as_view(),name='index'),
]