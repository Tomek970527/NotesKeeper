from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('board/<str:pk>/', views.board, name="board"),
    path('create-board/', views.create_board, name="create-board"),
    path('update-board/<str:pk>', views.update_board, name="update-board"),
    path('delete-board/<str:pk>', views.delete_board, name="delete-board"),
    path('note/<str:pk>/', views.note, name="note"),
    path('create-note/<str:pk>', views.create_note, name="create-note"),
    path('update-note/<str:pk>', views.update_note, name="update-note"),
    path('delete-note/<str:pk>', views.delete_note, name="delete-note"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
]
