A continuación, se proporciona el código actualizado con la nueva función `agregar_prioridad` y las pruebas correspondientes:

```python
def agregar(tareas, titulo):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("Título obligatorio")
    tarea = {"id": len(tareas) + 1, "titulo": titulo, "prioridad": "media"}
    tareas.append(tarea)
    return tarea


def pendientes(tareas):
    return list(tareas)


def agregar_prioridad(tareas, titulo, prioridad):
    valid_priorities = ['alta', 'media', 'baja']
    if prioridad not in valid_priorities:
        raise ValueError(f"Prioridad '{prioridad}' no válida. Debe ser 'alta', 'media' o 'baja'.")
    tarea = {"id": len(tareas) + 1, "titulo": titulo, "prioridad": prioridad}
    tareas.append(tarea)


def filtrar_por_prioridad(tareas, prioridad):
    return [tarea for tarea in tareas if tarea['prioridad'] == prioridad]


# Pruebas válidas
tareas = []
agregar(tareas, "Tarea 1")
agregar_prioridad(tareas, "Tarea 2", "alta")
agregar_prioridad(tareas, "Tarea 3", "media")

# Pruebas inválidas
try:
    agregar_prioridad(tareas, "Tarea 4", "invalida")
except ValueError as e:
    print(e)  # Debería imprimir "Prioridad 'invalida' no válida. Debe ser 'alta', 'media' o 'baja'."

# Pruebas de regresión
print(pendientes(tareas))  # Debería imprimir [{'id': 1, 'titulo': 'Tarea 1', 'prioridad': 'media'}, {'id': 2, 'titulo': 'Tarea 2', 'prioridad': 'alta'}, {'id': 3, 'titulo': 'Tarea 3', 'prioridad': 'media'}]
```

### Explicación de Pruebas:

1. **Pruebas Válidas:**
   - Se agregan tareas con diferentes prioridades ('media', 'alta', 'media') y se verifica que se agregan correctamente a la lista de tareas.

2. **Pruebas Inválidas:**
   - Se intenta agregar una tarea con una prioridad inválida ('invalida') y se verifica que se lanza un `ValueError` con el mensaje correcto.

3. **Pruebas de Regresión:**
   - Se verifica que la función `pendientes` devuelve la lista de tareas con todas las prioridades agregadas correctamente.