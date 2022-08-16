from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('watchlist/',views.show_watchlist, name='show_watchlist'),
    path('close_list/<int:id>',views.close_list,name='close_list'),
    path('closed_listings',views.show_closed_listing,name='show_closed_listing'),
    path('add/listing', views.create_listing, name="add-listing"),
    path('add/category', views.add_category, name="add-category"),
    path('categoryList/', views.category_list, name="category-list"),
    path('categoryList/show/<id>', views.show_category, name="show-category"),
    path('post/<int:id>', views.show_listing , name='show_list'),
    path('add_to_watchlist/<int:id>',views.watchlist, name= 'watchlist_button')
]