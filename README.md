# Gestor de tareas con prioridad (lab multiagente)

Aplicación mínima en Python con un flujo de tres agentes (Planificador,
Implementador, Revisor) y un cuarto agente opcional (Documentador). El
requisito de negocio se obtiene de un servidor MCP de solo lectura y los
cambios se aplican **manualmente**, tras revisión humana.

## Uso

```python
from tareas import agregar, pendientes, filtrar_por_prioridad

tareas = []
agregar(tareas, "Leer")                  # prioridad "media" por defecto
agregar(tareas, "Entregar", "alta")      # "alta" | "media" | "baja"
filtrar_por_prioridad(tareas, "alta")    # [{'id': 2, ...}]
```

- `agregar(tareas, titulo, prioridad="media")` → diccionario de la tarea.
  Título vacío o prioridad no permitida → `ValueError`.
- `pendientes(tareas)` → copia de la lista (la API original se conserva).
- `filtrar_por_prioridad(tareas, prioridad)` → tareas con esa prioridad.

## Requisito (obtenido por MCP)

`mcp_requisitos.py` expone la tool `requisito_prioridad` con `MCPServer`.
`multiagentes.py` la consulta con `mcp.Client` (transporte en memoria) y
propaga el texto a los agentes locales de Ollama.

```bash
python verificar_mcp.py     # lista tools y llama requisito_prioridad
```

## Flujo multiagente

```bash
python multiagentes.py      # modos: proponer | revisar | documentar
```

Cada fase escribe su salida en `evidencias/`:

| Archivo | Agente |
|---|---|
| `01_plan.md` | Planificador (pasos y criterios de aceptación) |
| `02_propuesta.md` | Implementador (código propuesto) |
| `03_revision.md` | Revisor (requisito, seguridad, pruebas) |
| `04_readme_propuesta.md` | Documentador (propone README) |

Los agentes **no** escriben en el repositorio ni ejecutan comandos: la persona
revisa, aplica el cambio acotado y vuelve a ejecutar las pruebas. Este README
fue aplicado a mano a partir de `04_readme_propuesta.md`.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

10 pruebas: 2 de base intactas y 8 nuevas (valor por defecto, prioridad válida,
normalización, prioridad inválida, prioridad no textual, filtro, filtro
inválido y regresión del contrato antiguo).

## CI y entrega

`.github/workflows/ci.yml`:

- `test` en cada PR y push a `main` con Python 3.12.
- `delivery` solo tras push a `main` y con `test` verde: compila `tareas.py` y
  publica el artefacto `paquete-lab`.

Empaquetar un artefacto **no** es desplegar: no hay publicación en ningún
entorno de producción.

## Modelo local

Valor por defecto `qwen2.5-coder:3b`; se puede cambiar con la variable
`MODELO_LAB`. En esta ejecución se usó `qwen2.5-coder:3b` sobre un segundo
servidor Ollama (`OLLAMA_HOST`) con los modelos en otro disco.
