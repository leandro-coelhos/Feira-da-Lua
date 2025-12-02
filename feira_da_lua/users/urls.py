from django.urls import path
from .views import *

urlpatterns = [
     path("login/", LoginUser, name="login_user"),
     path("register/", RegisterUser, name="register_user"),
     path("logout/", LogoutUser, name="logout_user"),
     path("profile/<int:user_id>/", ProfileUser, name="profile_user"),
     path("comment/create/", CreateComment, name="create_comment"),
     path("comment/delete/", DeleteComment, name="delete_comment"),
     path("comment/update/", UpdateComment, name="update_comment"),
     path("comment/list/", ListComments, name="list_comments"),
]