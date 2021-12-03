
from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('add/<int:pk>', basketapp.add, name='add'),
    # path('remove/', basketapp.remove, name='remove'),
]
