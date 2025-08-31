from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post URLs
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('my-posts/', views.my_posts, name='my_posts'),
    
    # Post detail with date-based URL
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.PostDetailView.as_view(), name='post_detail'),
    
    # Post management URLs (using pk for simplicity in edit/delete)
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]