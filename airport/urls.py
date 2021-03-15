from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_data, name="list_data"),
    path('create', views.create_data, name="create_data"),
    path('delete/<int:airport_id>', views.delete_data, name="delete_data"),
    path('update/<int:airport_id>', views.update_data, name="update_data"),
]