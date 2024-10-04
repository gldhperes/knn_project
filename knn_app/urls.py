from django.urls import path
from .views import previsao_view

urlpatterns = [
    path('', previsao_view, name='previsao'),
]
