from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('register-api/', views.RegisterUserAPI.as_view(), name='sign_up'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/user/login'), name='logout'),
    path('user-api/', views.UserAPIView.as_view()),
    path('user-api/<str:user_id>/', views.UserDetailAPIView.as_view()),
    path('follow-api/<str:user_id>/', views.FollowAPI.as_view()),
    path('become-fan-api/<str:user_id>/', views.BecomeFanAPI.as_view()),
    path('gift-api/<str:receiver_name>/<int:gift_code>/', views.GiftAPI.as_view())
]
