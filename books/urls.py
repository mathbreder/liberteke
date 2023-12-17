from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='all'),
    path('<int:pk>', views.BookDetailView.as_view(), name='detail'),
    path('create', views.BookCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.BookUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.BookDeleteView.as_view(), name='delete'),
    path('export', views.BookExportView.as_view(), name='export'),
]
