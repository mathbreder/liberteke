from django.urls import path
from . import views

app_name = 'genres'

urlpatterns = [
    path('', views.GenreListView.as_view(), name='all'),
    path('<int:pk>', views.GenreDetailView.as_view(), name='detail'),
    path('create', views.GenreCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.GenreUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.GenreDeleteView.as_view(), name='delete'),
]
