from django.urls import path
from smart_irrigation.data.views import CreateDataView


urlpatterns = [
    path('', CreateDataView.as_view(), name='data-creation'),
]
