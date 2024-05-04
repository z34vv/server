from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('my-messages/', views.MyInbox.as_view()),
    path('get-messages/<str:receiver_id>/', views.MessagesAPI.as_view()),
    path('search/<str:username>/', views.SearchUserAPI.as_view()),
    path('', views.ChatView.as_view(), name="chat"),
    path('<str:username>/', views.ChatBox.as_view(), name='chat-box'),
    path('send-msg/<str:partner_name>', views.sendMessage, name="send-msg"),
    path('<str:receiver_name>/donate-gift/<int:gift_code>/', views.donateGift, name='donate-gift'),
    path('search-user/', views.searchUser, name='msg-search-user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
