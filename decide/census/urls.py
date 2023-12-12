from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('exportar_censo/', views.CensusExport.as_view(), name='exportar_censo'),
    path('importar_censo/', views.ImportCensus.as_view(), name='importar_censo'),
]
