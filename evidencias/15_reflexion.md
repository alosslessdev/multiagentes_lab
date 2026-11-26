# Reflexión y respuestas (Laboratorio 16)

## Qué hizo cada agente, qué hizo MCP, qué automatizó CI y qué aprobó la persona

El Planificador recibió el requisito desde la tool MCP `requisito_prioridad` y
produjo pasos, criterios de aceptación y un plan de pruebas en
`evidencias/01_plan.md`; no escribió código ejecutable en el repositorio. El
Implementador propuso código y pruebas en `evidencias/02_propuesta.md`; su
propuesta fue defectuosa (creó `agregar_prioridad` en vez de extender
`agregar` y llamó "pruebas" a sentencias sueltas), por lo que la persona aplicó
solo el cambio acotado: `agregar(tareas, titulo, prioridad="media")`,
validación con `ValueError` y `filtrar_por_prioridad`. El Revisor recibió
requisito, código, tests y la salida real de `unittest` y emitió su informe sin
ejecutar nada. El Documentador propuso un README a partir del plan y del código
aprobado; el README final se escribió a mano. MCP aportó la especificación de
negocio de solo lectura, con procedencia verificable. CI automatizó lo
determinista: ejecutar `unittest` en un runner limpio con Python 3.12 en cada PR
y push, y tras el merge compilar `tareas.py` y publicar el artefacto
`paquete-lab`. La persona aprobó el diff, aplicó los cambios, rechazó la
propuesta inválida, verificó la prueba de rechazo y autorizó el merge. Ningún
agente hizo push, commit ni ejecutó comandos.

(≈190 palabras)

## 1. ¿Por qué tres agentes y no tres prompts sin roles ni traspasos?

Porque los roles separan responsabilidades y hacen auditable el traspaso: el
Planificador solo define criterios, el Implementador solo propone código y el
Revisor solo evalúa con evidencia de pruebas. Cada fase deja un artefacto en
disco (`01_plan.md`, `02_propuesta.md`, `03_revision.md`) que la persona revisa
y que puede regenerarse de forma aislada. Tres prompts en una sola sesión
mezclarían criterios, no dejarían rastro verificable y permitirían que la misma
respuesta se autoapruebe. El traspaso por archivos **no** es aprobación
automática: es material de revisión.

## 2. ¿Qué obtiene el Planificador por MCP y por qué es de solo lectura?

Obtiene el requisito de negocio autorizado: prioridades permitidas, valor por
defecto, rechazo con `ValueError`, función de filtrado, conservación de la API y
pruebas exigidas. Es de solo lectura porque es la fuente de verdad aprobada: un
agente no debe poder reescribir la especificación para que su propio código
"cumpla", y una tool que solo devuelve texto no puede convertirse en vector de
ejecución ni de escritura. La salida de MCP es dato externo, sin autoridad para
ordenar despliegues ni revelar secretos.

## 3. ¿Qué debe hacer el desarrollador si Implementador y Revisor discrepan?

Decidir con evidencia, no con la confianza en el texto: ejecutar
`python -m unittest discover -s tests -v`, comparar el código con los criterios
de aceptación del plan y con el requisito MCP, y revisar el diff. Si el Revisor
afirma que todo pasa sin mostrar resultados, se descarta esa afirmación; si el
Implementador viola el requisito, se rechaza su propuesta. Después se reformulan
las instrucciones del rol implicado, se regenera la fase y se documenta la
decisión en el PR. Nunca se marca "aprobado" con pruebas en rojo.

## 4. ¿Qué valida CI realmente y qué no garantiza una prueba verde?

CI valida que el repositorio, en un runner limpio con la versión de Python
declarada, instala lo necesario y que las pruebas comprometidas pasan; también
que el empaquetado posterior compila `tareas.py`. No garantiza que el requisito
esté bien interpretado, que las pruebas sean significativas, que no falten casos
(borrados, concurrencia, datos reales), ni la calidad del texto del LLM. Una
prueba verde solo prueba lo que esa prueba afirma.

## 5. Diferencia entre PR, merge, entrega de artefacto y despliegue

- **PR**: propuesta de cambio con diff, discusión y checks; todavía no está en `main`.
- **Merge**: integración del cambio en la rama principal, con historial y revisión.
- **Entrega de artefacto**: el job `delivery` compila y publica `paquete-lab`
  como archivo descargable, reproducible y versionado.
- **Despliegue**: publicar y ejecutar ese paquete en un entorno real (staging o
  producción), con configuración, secretos y aprobación operativa.

Empaquetar **no** es desplegar: en este laboratorio no se publica en ningún
entorno externo.

## 6. ¿Qué permisos no debe otorgar el laboratorio?

A los agentes: escritura en el repositorio, push, merge, ejecución arbitraria de
comandos, acceso a secretos, tokens o datos personales, y cualquier capacidad de
despliegue. Al `GITHUB_TOKEN`: `contents: write`, `actions: write`, `packages:
write`, `deployments`, `id-token` o administración; el workflow declara solo
`contents: read`. El servidor MCP no debe conectarse a sistemas bancarios,
correo, servicios de producción ni credenciales.
