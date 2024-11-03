from django.db import models
from django.conf import settings  # Para referenciar al usuario actual
from django.contrib.auth.models import AbstractUser

# Definición del usuario personalizado
class Usuario(AbstractUser):
    es_establecimiento = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text="Los grupos a los que pertenece este usuario.",
        verbose_name="grupos",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text="Permisos específicos para este usuario.",
        verbose_name="permisos de usuario",
    )

# Definición de categorías para los servicios
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Establecimientos que ofrecen servicios
class Establecimiento(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="establecimiento")
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

# Servicios ofrecidos por establecimientos
class Servicio(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, related_name="servicios")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion = models.DurationField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="servicios")  # Relación con Categoria

    def __str__(self):
        return f"{self.nombre} - {self.establecimiento.nombre}"

# Modelo de reserva para servicios
class Reserva(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="reservas")
    fecha_hora = models.DateTimeField()
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva de {self.cliente.username} para {self.servicio.nombre} en {self.fecha_hora}"

# Modelo de carrito para un usuario con múltiples servicios
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="carritos")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

# Detalles de cada ítem del carrito
class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} de {self.servicio.nombre}"

    def subtotal(self):
        return self.servicio.precio * self.cantidad

