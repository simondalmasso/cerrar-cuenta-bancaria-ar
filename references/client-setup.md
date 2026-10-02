# Conexión a agentes

La skill no depende de una empresa de IA. El contenido canónico es esta carpeta.

## Regla

Instalar **una sola copia** del repo en la ubicación de skills que lea el host. No mantener versiones divergentes para cada proveedor.

## Codex / OpenAI

Codex usa el estándar abierto Agent Skills y descubre skills de repositorio en `.agents/skills`.

Ejemplo:
```
PROYECTO/
  .agents/
    skills/
      cerrar-cuenta-bancaria-ar/
        SKILL.md
        references/
        assets/
```

También puede instalarse a nivel usuario según la documentación vigente del host.

## Gemini CLI

Gemini CLI implementa Agent Skills y admite `.agents/skills/` como alias de su ruta de skills de workspace/usuario.

La misma carpeta funciona sin reescribir SKILL.md.

## Claude Code / Claude Agent SDK

Claude usa el mismo formato SKILL.md, normalmente desde `.claude/skills/` o directorios de skills habilitados por el host.

Copiar o enlazar la misma carpeta:
```
.claude/
  skills/
    cerrar-cuenta-bancaria-ar/
```

## Cursor / VS Code / otros clientes compatibles

Si el cliente soporta el estándar Agent Skills, apuntarlo a esta misma carpeta. Si no lo soporta, cargar SKILL.md como instrucciones persistentes y permitir lectura de references/.

## Chat sin filesystem

Pegar o adjuntar SKILL.md y, cuando la rama lo requiera, el archivo de references correspondiente.

Prompt mínimo:
> Usá la skill cerrar-cuenta-bancaria-ar. Guiame, pero no operes mi banco, navegador, home banking, dinero ni reclamos externos por mí.

## MCP

MCP no instala la skill. MCP agrega fuentes/herramientas.

La separación correcta es:
- Skill = criterio y protocolo.
- MCP = investigación jurídica read-only.
- Humano = toda operación bancaria.

Ver integrations.md.
