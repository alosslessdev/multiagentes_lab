"""Orquestador multiagente (Planificador -> Implementador -> Revisor -> Documentador).

La IA solo propone texto en evidencias/. Ningún agente escribe en el
repositorio ni ejecuta comandos: la persona revisa y aplica los cambios.

Uso:
    python multiagentes.py            # pregunta el modo
    echo proponer | python multiagentes.py
Modos: proponer | revisar | documentar
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

from mcp import Client
from mcp.types import TextContent
from ollama import chat

from mcp_requisitos import mcp

MODELO = os.environ.get("MODELO_LAB", "qwen2.5-coder:7b")
EVID = Path("evidencias")
EVID.mkdir(exist_ok=True)


async def leer_requisito() -> str:
    async with Client(mcp) as cliente:
        herramientas = await cliente.list_tools()
        nombres = [h.name for h in herramientas.tools]
        if "requisito_prioridad" not in nombres:
            raise RuntimeError(f"Falta requisito_prioridad en MCP: {nombres}")
        resultado = await cliente.call_tool("requisito_prioridad", {})
        if resultado.is_error:
            raise RuntimeError("Falló la herramienta MCP")
        texto = "\n".join(
            x.text for x in resultado.content if isinstance(x, TextContent)
        )
        (EVID / "00_requisito_mcp.txt").write_text(
            "tools: " + ", ".join(nombres) + "\n\n" + texto + "\n",
            encoding="utf-8",
        )
        return texto


def consultar(rol: str, instruccion: str, datos: str) -> str:
    respuesta = chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": instruccion},
            {"role": "user", "content": datos},
        ],
        options={"temperature": 0.2, "num_ctx": 8192, "num_predict": 900},
    )
    return respuesta.message.content or ""


async def proponer() -> None:
    req = await leer_requisito()
    base = Path("tareas.py").read_text(encoding="utf-8")
    plan = consultar(
        "planificador",
        "Eres planificador. Define pasos, criterios de aceptación y pruebas. "
        "No escribas código ni inventes requisitos.",
        "REQUISITO MCP:\n" + req + "\nCÓDIGO:\n" + base,
    )
    (EVID / "01_plan.md").write_text(plan, encoding="utf-8")
    propuesta = consultar(
        "implementador",
        "Eres implementador. Propón tareas.py y tests completos. "
        "Conserva la API antigua; no uses paquetes externos. "
        "Devuelve solo bloques de código Python.",
        "REQUISITO:\n" + req + "\nPLAN:\n" + plan
        + "\nCÓDIGO ACTUAL:\n" + base,
    )
    (EVID / "02_propuesta.md").write_text(propuesta, encoding="utf-8")
    print("Revise evidencias/01_plan.md y evidencias/02_propuesta.md.")


async def revisar() -> None:
    req = await leer_requisito()
    pruebas = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    evidencia = (
        "REQUISITO:\n" + req
        + "\nCÓDIGO:\n" + Path("tareas.py").read_text(encoding="utf-8")
        + "\nTESTS:\n" + Path("tests/test_tareas.py").read_text(encoding="utf-8")
        + "\nRESULTADO:\n" + pruebas.stdout + pruebas.stderr
    )
    informe = consultar(
        "revisor",
        "Evalúa requisito, seguridad y pruebas. Señala faltantes; "
        "no afirmes que todo pasa si no hay evidencia.",
        evidencia,
    )
    (EVID / "03_revision.md").write_text(informe, encoding="utf-8")
    print("Exit code pruebas:", pruebas.returncode)
    print("Revise evidencias/03_revision.md")


async def documentar() -> None:
    plan = (EVID / "01_plan.md").read_text(encoding="utf-8")
    codigo = Path("tareas.py").read_text(encoding="utf-8")
    propuesta = consultar(
        "documentador",
        "Eres documentador. Redacta un README en Markdown a partir del plan y "
        "del código aprobado. No inventes funciones ni requisitos.",
        "PLAN:\n" + plan + "\nCÓDIGO APROBADO:\n" + codigo,
    )
    (EVID / "04_readme_propuesta.md").write_text(propuesta, encoding="utf-8")
    print("Revise evidencias/04_readme_propuesta.md (no se escribe README.md).")


MODOS = {"proponer": proponer, "revisar": revisar, "documentar": documentar}

if __name__ == "__main__":
    modo = input("Modo (proponer/revisar/documentar): ").strip()
    if modo not in MODOS:
        raise SystemExit(f"Modo inválido: {modo!r}. Use {', '.join(MODOS)}.")
    print("Modelo:", MODELO)
    asyncio.run(MODOS[modo]())
