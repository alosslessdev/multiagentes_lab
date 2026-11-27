# Evidencia de PR, CI y entrega

- Repositorio (público desde 2026-11-27): https://github.com/alosslessdev/multiagentes_lab
- PR #1: https://github.com/alosslessdev/multiagentes_lab/pull/1 — **MERGED**
  (merge commit `666affeb355421da0f1c358a51752600a63727c4`).
- Comentario de revisión cruzada:
  https://github.com/alosslessdev/multiagentes_lab/pull/1#issuecomment-7181017870

## Checks del PR

| Commit | Job `test` | Job `delivery` | Run |
|---|---|---|---|
| `ce7a1e8` (propuesta inicial) | pass | skipping (PR) | 45743706662 |
| `77c16e0` (prueba de rechazo) | **fail** — `AssertionError: ValueError not raised` (2 fallos) | skipping | 45743787660 |
| `5ea7309` (validación restaurada) | pass | skipping | 45743856682 |
| `1aff073` (prueba no textual) | pass | skipping | 45743931331 |

Log del fallo bloqueado por CI: `evidencias/12_fallo_intencional_ci.txt`.
Prueba local del mismo fallo: `evidencias/11_fallo_intencional_local.txt`.

## Entrega tras el merge

Run de `main`: 45744010172 — `test` success, `delivery` success.
Run posterior de documentación: 45744231030 — `test` success, `delivery` success.
Artefacto `paquete-lab` (id 15082571587) descargado a `artefacto/tareas.py`:

```
954 B  tareas.py
sha256 75b4a7659bec36e7c94153b06026d83a9376b855182ed190613cb507a7544917
```

Comprobación local: `py_compile` del archivo descargado sin errores; es idéntico
al `tareas.py` de `main` (mismo tamaño y hash).

**Empaquetar no es desplegar**: el job `delivery` no publica en ningún entorno,
solo genera el artefacto descargable. No hay URL de producción ni credenciales
involucradas.

Control de seguridad previo a publicar: `evidencias/17_seguridad.txt`
(`subprocess.run` solo ejecuta el comando fijo de pruebas, nunca texto del modelo).
