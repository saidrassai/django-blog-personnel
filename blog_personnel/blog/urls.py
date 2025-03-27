from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/new/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # Add these new URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('my-articles/', views.UserArticlesView.as_view(), name='user-articles'),
]