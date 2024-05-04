from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('user/', include('User.urls')),
    path('', include('Post.urls')),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('chat/', include('Chat.urls')),
    # path('management/', include('Management.urls')),
    # path('recharge/', include('Recharge.urls')),
]
