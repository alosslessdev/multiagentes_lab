# Prioridad en gestor de tareas (multiagente + MCP + CI)

## Objetivo

Agregar prioridad (`alta`/`media`/`baja`, por defecto `media`), validación con
`ValueError` y `filtrar_por_prioridad(tareas, prioridad)`, conservando
`agregar(tareas, titulo)` y `pendientes(tareas)`.

## Requisito extraído por MCP

Servidor: `mcp_requisitos.py` (`MCPServer("RequisitosLab")`, tool `requisito_prioridad`).
Llamada real vía `mcp.Client`, transporte en memoria; `is_error == False`.
Salida completa en `evidencias/00_llamada_mcp.txt` y `evidencias/00_requisito_mcp.txt`.

## Cambios

- `tareas.py`: `PRIORIDADES`, `_normalizar_prioridad`, `agregar(..., prioridad="media")`,
  `filtrar_por_prioridad`.
- `tests/test_tareas.py`: 10 pruebas (2 de base intactas + 8 nuevas: prioridad válida, valor por defecto,
  normalización, inválida, no textual, filtro, filtro inválido, regresión).
- `mcp_requisitos.py`, `verificar_mcp.py`, `multiagentes.py` (Planificador →
  Implementador → Revisor → Documentador; la IA solo escribe en `evidencias/`).
- `.github/workflows/ci.yml`: job `test` en PR/push y job `delivery` (artefacto
  `paquete-lab`) solo tras push a `main`.

## Evidencias

- `evidencias/00_baseline.txt` — línea base (2 pruebas OK).
- `evidencias/00_llamada_mcp.txt` — tools listadas y contenido del requisito.
- `evidencias/01_plan.md` — Planificador.
- `evidencias/02_propuesta.md` — Implementador.
- `evidencias/03_revision.md` — Revisor (con resultado de pruebas).
- `evidencias/04_readme_propuesta.md` — Documentador.
- `evidencias/05_pruebas_despues.txt` — pruebas OK tras aplicar el cambio.
- `evidencias/06_ejecucion_proponer.log` — ejecución del orquestador.
- `evidencias/09_reflexion.md` — respuestas y reflexión.

## Pruebas ejecutadas

```
python -m unittest discover -s tests -v   # 9 tests, OK
python verificar_mcp.py                   # is_error: False
git diff --check                          # sin errores de whitespace
```

## Riesgos y decisiones humanas

- El requisito no fija normalización de mayúsculas/espacios; se acepta
  `" ALTA "` como `"alta"` para robustez de entrada. Decisión humana documentada.
- `id = len(tareas) + 1` es preexistente: tras borrar tareas puede repetirse.
  No se cambió por estar fuera del requisito.
- La propuesta del modelo local se revisó y se aplicó **manualmente**; el agente no
  tiene escritura en el repositorio ni ejecuta comandos.
- CI valida solo el resultado determinista; no valida la calidad del texto del LLM.

## Checklist

- [x] Requisito obtenido por MCP de solo lectura
- [x] Prioridad con valor por defecto y validación
- [x] `filtrar_por_prioridad` implementado
- [x] Pruebas nuevas + base verdes en local
- [x] Workflow con permisos mínimos (`contents: read`)
- [x] Sin secretos, tokens ni datos personales
- [x] Artefacto de entrega generado tras merge
