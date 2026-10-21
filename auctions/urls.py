from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.create_listing, name="createlist"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watchlist/add",views.add, name="add"),
    path("watchlist/remove", views.remove, name="remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("close", views.closelisting, name="close"),
    path("bought", views.boughtitems, name="bought"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categoricallist/<str:category>", views.categoricallist, name="categoricallist"),
]
