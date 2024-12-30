from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:show_id>/', views.book_tickets, name='book_tickets'),
]
