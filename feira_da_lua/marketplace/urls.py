from django.urls import path
from .views import home, marketplace_detail, toggle_favorite, add_review, update_review, delete_review, my_fairs, create_fair, edit_fair, gps_location

urlpatterns = [
    path('', home, name='home'),
    path('gps/', gps_location, name='gps_location'),
    path('minhas-feiras/', my_fairs, name='my_fairs'),
    path('minhas-feiras/nova/', create_fair, name='create_fair'),
    path('minhas-feiras/editar/<int:marketplace_id>/', edit_fair, name='edit_fair'),
    path('feira/<int:marketplace_id>/', marketplace_detail, name='marketplace_detail'),
    path('feira/<int:marketplace_id>/avaliar/', add_review, name='add_review'),
    path('avaliacao/<int:review_id>/editar/', update_review, name='update_review'),
    path('avaliacao/<int:review_id>/apagar/', delete_review, name='delete_review'),
    path('favorito/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
]


