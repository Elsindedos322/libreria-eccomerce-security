from django.contrib import admin
from .models import Libro, Categoria, Autor,Editorial

admin.site.register(Libro)
admin.site.register(Categoria)
admin.site.register(Autor)
admin.site.register(Editorial)

