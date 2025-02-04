from django.urls import path
from .views import BoothView, StaticViews


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('register/', BoothView.registerPage, name='register'),
    path('thanks/', StaticViews.GiveThanks, name='thanks'),
    path('home/', BoothView.homePage, name='home'),
    path('change_user/', BoothView.change_user, name='change_user'),
    path('1/', BoothView.as_view(), name='initialBooth'),
]

