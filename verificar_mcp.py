"""Prueba directa del servidor MCP: lista tools y llama requisito_prioridad.

No forma parte de tests/ a propósito: el runner de CI no instala MCP.
Uso: python verificar_mcp.py
"""

import asyncio

from mcp import Client
from mcp.types import TextContent

from mcp_requisitos import mcp


async def main() -> None:
    async with Client(mcp) as cliente:
        tools = await cliente.list_tools()
        for t in tools.tools:
            print("tool:", t.name, "|", (t.description or "").strip())
        resultado = await cliente.call_tool("requisito_prioridad", {})
        print("is_error:", resultado.is_error)
        textos = [x.text for x in resultado.content if isinstance(x, TextContent)]
        print("content:", textos)
        assert not resultado.is_error
        assert textos and "filtrar_por_prioridad" in textos[0]


if __name__ == "__main__":
    asyncio.run(main())
