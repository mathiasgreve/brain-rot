from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_entry, name='add_entry'),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout views
    path('login/', auth_views.LoginView.as_view(next_page='home'), name='login'),    # stock view - change ?
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # stock view - change?
    path('signup/', views.signup, name='signup'),  # Add this line for the signup page
    path('upvote/<int:entry_id>/', views.upvote_entry, name='upvote_entry'),
    path('downvote/<int:entry_id>/', views.downvote_entry, name='downvote_entry'),
]
