from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('writeblog',views.writeblog,name='writeblog'),
    path('article/<int:id>',views.article,name='article'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('category/<str:category>', views.category, name='category'),
    path('comment', views.comment, name='comment'),
    path('search', views.search, name='search'),
    path('delete<int:id>', views.delete, name='delete'),

]