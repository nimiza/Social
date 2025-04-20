from . import views
from django.urls import path


app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/write/', views.PostWriteView.as_view(), name='post_write'),
    path('posts/like/<int:post_id>', views.PostLikeView.as_view(), name='post_like'),
    path('reply/<int:post_id>/<int:comment_id>/', views.ReplyWriteView.as_view(), name='reply_write'),
]
