from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<str:username>/', views.perfil_view, name='perfil'),
    path('editar-perfil/', views.editar_perfil_view, name='editar_perfil'),
    path('buscar/', views.buscar, name='buscar'),
     path('ajax/buscar/', views.buscar_ajax, name='buscar_ajax'),
    path('nova-postagem/', views.nova_postagem, name='nova_postagem'),
    path('curtir-post/', views.curtir_post, name='curtir_post'),

]
