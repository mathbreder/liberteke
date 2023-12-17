from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='all'),
    path('<int:pk>', views.AuthorDetailView.as_view(), name='detail'),
    path('create', views.AuthorCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.AuthorUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.AuthorDeleteView.as_view(), name='delete'),
]
