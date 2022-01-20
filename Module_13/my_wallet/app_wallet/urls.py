from django.urls import path

from . import views


app_name = 'app_wallet'


urlpatterns = [
    path('home', views.homepage, name='homepage'),
    path('register', views.register_request, name='register'),
    path('', views.login_request, name='login'),
    path('add', views.add_request, name='add'),
    path('show', views.show_request, name='show'),
    path('edit', views.edit_request, name='edit'),
    path('find', views.find_request, name='find'),
    path('delete', views.delete_request, name='delete'),
    path('logout', views.logout_request, name='logout'),
]
