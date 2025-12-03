from django.urls import path
from .views import *

urlpatterns = [
     path("index/", IndexPage, name="index"),
     path("login/", LoginUser, name="login"),
     path("registro/", RegistroPage, name="registro"),
     path("register/", RegisterUser, name="register_user"),
     path("register/feirante/", RegisterMarketer, name="register_marketer"),
     path("logout/", LogoutUser, name="logout"),
     path("favoritos/", FavoritesPage, name="favorites"),
     path("profile/", ProfileUser, name="profile_user"),
     path("user/delete/", DeleteUser, name="delete_user"),
     path("user/update/", UpdateUser, name="update_user"),
     path("user/list/", ListUsers, name="list_users"),
     path("comment/create/", CreateComment, name="create_comment"),
     path("comment/delete/", DeleteComment, name="delete_comment"),
     path("comment/update/", UpdateComment, name="update_comment"),
     path("comment/list/", ListComments, name="list_comments"),
]