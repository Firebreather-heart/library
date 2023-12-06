from django.urls import path 
from . import views 
urlpatterns = [
    path('', views.GetBookPaginatorView.as_view(), name='books'),
    path('add/', views.AddBookApiView.as_view(), name="add_book"),
    path('library/<uuid:id>/', views.GetBookApiview.as_view(), name='get_book'),
    path('categories/', views.GetCategoryListApiVIew.as_view(), name='get_categories'),
]