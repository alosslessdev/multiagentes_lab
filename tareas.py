PRIORIDADES = ("alta", "media", "baja")
PRIORIDAD_POR_DEFECTO = "media"


def _normalizar_prioridad(prioridad):
    # PRUEBA DE RECHAZO: validación desactivada a propósito.
    return prioridad.strip().lower() if isinstance(prioridad, str) else prioridad


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
