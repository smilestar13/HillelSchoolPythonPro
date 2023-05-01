from django.urls import path, re_path

from wishes.views import WishView, WishActionView

urlpatterns = [
    path('favourites/', WishView.as_view(), name='favourites'),
    re_path(r'favourites/(?P<action>add|remove|clear|pay)/',
            WishActionView.as_view(),
            name='wish_list_action'),
]
