from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing_view, name="add_listing"),
    path("listing/<int:id>", views.listing_view, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.specific_category, name="specific_category"),
]
