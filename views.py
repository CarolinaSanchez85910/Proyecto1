from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Servicio, Carrito, DetalleCarrito
from django.contrib.auth.decorators import login_required

def inicio(request):
    return render(request, 'principal/inicio.html')

def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    servicios = Servicio.objects.filter(categoria=categoria)
    return render(request, 'principal/categoria.html', {'categoria': categoria, 'servicios': servicios})

def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    return render(request, 'principal/detalle_servicio.html', {'servicio': servicio})

@login_required
def agregar_al_carrito(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    detalle, detalle_creado = DetalleCarrito.objects.get_or_create(carrito=carrito, servicio=servicio)
    if not detalle_creado:
        detalle.cantidad += 1
    detalle.save()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'principal/ver_carrito.html', {'carrito': carrito})

@login_required
def eliminar_del_carrito(request, detalle_id):
    detalle = get_object_or_404(DetalleCarrito, id=detalle_id, carrito__usuario=request.user)
    detalle.delete()
    return redirect('ver_carrito')

