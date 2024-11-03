from django.urls import path
from . import views

urlpatterns = [
    # Rutas de página principal
    path('', views.inicio, name='inicio'),
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),
    path('servicio/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    
    # Rutas del carrito de compras
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:servicio_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:detalle_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
]

