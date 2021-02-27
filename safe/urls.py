from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('savedpasswords/', views.SavedListView.as_view(), name='saved'),
    path('generatepasswords/', views.generate_password, name='gen_pass'),
    path('add_password/', views.PasswordAddView.as_view(), name='add_pass'),
]