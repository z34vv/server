from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('post/', include(router.urls)),
    path('post-api/', views.PostAPIView.as_view(), name='post-api'),
    path('post-api/<int:pk>/', views.PostDetailAPIView.as_view()),
    path('new-feed/', views.NewFeedAPIView.as_view(), name='new-feed-api'),
    path('comment-api/<int:post_id>/', views.PostCommentApiView.as_view(), name='comment-api'),
    path('like-post/<int:post_id>/', views.PostLike.as_view(), name='like-post-api'),
    path('like-cmt/<int:cmt_id>/', views.CommentLike.as_view(), name='like-cmt-api'),
    path('rep-cmt-api/<int:post_id>/<int:cmt_id>/', views.RepPostCommentApiView.as_view()),
    path('rep-cmt-like/<int:rep_cmt_id>/', views.RepCommentLike.as_view()),
    path('', views.HomeView.as_view(), name='home'),
]
