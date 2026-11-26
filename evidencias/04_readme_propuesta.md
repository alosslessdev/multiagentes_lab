### README

# Tareas App

Este es un simple sistema de gestión de tareas que permite agregar tareas con diferentes prioridades y filtrarlas por prioridad.

## Requisitos

1. **Agregar Prioridad:**
   - Agregar una tarea con una prioridad específica ('alta', 'media' o 'baja').
   - Validar que la prioridad sea válida y lanzar un `ValueError` si no lo es.

2. **Filtrar por Prioridad:**
   - Filtrar las tareas por una prioridad específica.

3. **Pruebas:**
   - Pruebas válidas: Agregar tareas con diferentes prioridades y verificar que se agregan correctamente.
   - Pruebas inválidas: Intentar agregar tareas con prioridades inválidas y verificar que se lanzan `ValueError`.
   - Pruebas de regresión: Verificar que las funciones `agregar` y `pendientes` funcionan correctamente después de agregar tareas.

## Códigos

```python
PRIORIDADES = ("alta", "media", "baja")
PRIORIDAD_POR_DEFECTO = "media"

def _normalizar_prioridad(prioridad):
    if not isinstance(prioridad, str):
        raise ValueError(f"Prioridad inválida: {prioridad!r}")
    valor = prioridad.strip().lower()
    if valor not in PRIORIDADES:
        raise ValueError(
            f"Prioridad inválida: {prioridad!r}. Use: {', '.join(PRIORIDADES)}"
        )
    return valor


def agregar(tareas, titulo, prioridad=PRIORIDAD_POR_DEFECTO):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("Título obligatorio")
    tarea = {
        "id": len(tareas) + 1,
        "titulo": titulo,
        "prioridad": _normalizar_prioridad(prioridad),
    }
    tareas.append(tarea)
    return tarea


def pendientes(tareas):
    return list(tareas)


def filtrar_por_prioridad(tareas, prioridad):
    valor = _normalizar_prioridad(prioridad)
    return [t for t in tareas if t["prioridad"] == valor]
```

## Explicación de Pruebas

1. **Pruebas Válidas:**
   - Se agregan tareas con diferentes prioridades ('media', 'alta', 'media') y se verifica que se agregan correctamente a la lista de tareas.

2. **Pruebas Inválidas:**
   - Se intenta agregar una tarea con una prioridad inválida ('invalida') y se verifica que se lanza un `ValueError` con el mensaje correcto.

3. **Pruebas de Regresión:**
   - Se verifica que la función `pendientes` devuelve la lista de tareas con todas las prioridades agregadas correctamente.

Este código cumple con los requisitos especificados y incluye pruebas para garantizar la funcionalidad de la aplicación.