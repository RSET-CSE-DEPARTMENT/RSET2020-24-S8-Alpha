from django.urls import path
from .views import sse_stream, send_audio, GetUsersView, InitChatView, GetChatView, GetUserInfoView, GetOnlineStatus, SetOnlineStatus,\
    SetFavouriteUser, GetFavouriteUsers, RemoveFavouriteUser, Translate

urlpatterns = [
    path('init_chat/', InitChatView.as_view(), name = 'init_chat' ),
    path('get_chat_id/', GetChatView.as_view(), name = 'get_chat' ),
    path('get_online_status/', GetOnlineStatus.as_view(), name = 'get_status' ),
    path('set_online_status/', SetOnlineStatus.as_view(), name = 'set_status' ),
    path('set_favourite/', SetFavouriteUser.as_view(), name = 'set_favourite' ),
    path('get_favourites/', GetFavouriteUsers.as_view(), name = 'get_favourite' ),
    path('translate/', Translate.as_view(), name = "translate"),
    path('remove_favourite/<int:pk>/', RemoveFavouriteUser.as_view(), name = 'remove_favourite' ),
    path('get_user_info/<int:pk>/', GetUserInfoView.as_view(), name = 'get_user_info' ),
    path('search/', GetUsersView.as_view(), name = 'search_users' ),
    path('sse_stream/', sse_stream),
    path('send_audio/', send_audio)

]