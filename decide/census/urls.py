from django.urls import path, include
from . import views
from .views import importar_censo


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('exportar_censo/', views.CensusExport.as_view(), name='exportar_censo'),
    path('importar_censo/', importar_censo, name='importar_censo'),
]
