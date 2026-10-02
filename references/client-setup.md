# Conexión a agentes

La skill no depende de una empresa de IA. El contenido canónico es este repositorio y su manifiesto `SKILL.md`. `agents/openai.yaml` es metadata opcional de presentación para OpenAI y no altera el workflow portable.

## Regla

Instalar **una sola copia** de la skill. No mantener forks de contenido separados para cada proveedor.

## OpenAI / Codex / Agents

OpenAI documenta Agent Skills como carpetas con `SKILL.md` compatibles con el estándar abierto.

Para un workspace compatible con la convención de archivos:

```
PROYECTO/
  .agents/
    skills/
      cerrar-cuenta-bancaria-ar/
        SKILL.md
        references/
        assets/
```

La guía oficial de migración de OpenAI mapea `.claude/skills/*/SKILL.md` a `.agents/skills/*/SKILL.md`.

En Agents/Sandbox API también puede montarse el repo como fuente de la capability `Skills`, sin copiar manualmente la carpeta.

Fuentes:
- https://developers.openai.com/api/docs/guides/tools-skills
- https://developers.openai.com/api/docs/guides/agents/sandboxes
- https://developers.openai.com/cookbook/examples/agents_sdk/migrate-from-claude-agent-sdk/readme

## Gemini CLI

Gemini CLI implementa el estándar Agent Skills.

Rutas soportadas:
- usuario: `~/.gemini/skills/` o alias `~/.agents/skills/`;
- workspace: `.gemini/skills/` o alias `.agents/skills/`.

Instalación directa desde Git:

```bash
gemini skills install https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar --consent
```

Después:
```
/skills list
/skills reload
```

Fuentes:
- https://geminicli.com/docs/cli/skills/
- https://geminicli.com/docs/cli/tutorials/skills-getting-started/

## Claude Code / Claude Agent SDK

Anthropic usa el mismo formato portable `SKILL.md`.

Instalación manual típica a nivel usuario:

```bash
git clone https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git ~/.claude/skills/cerrar-cuenta-bancaria-ar
```

Anthropic documenta que los skills pueden reutilizarse entre Claude apps, Claude Code y API, y que Claude Code admite instalación manual bajo `~/.claude/skills`.

Fuente:
- https://www.anthropic.com/research/skills

## Otros hosts compatibles con Agent Skills

Si el cliente implementa el estándar, apuntarlo a esta misma carpeta.

Si no implementa discovery automático:
1. cargar `SKILL.md` como instrucciones;
2. permitir lectura de `references/` y `assets/`;
3. conservar las invariantes de seguridad;
4. no darle herramientas de operación bancaria.

## Chat sin filesystem

Adjuntar o pegar `SKILL.md`; aportar los archivos de `references/` solo cuando la rama del caso los necesite.

Prompt mínimo:

> Usá la skill cerrar-cuenta-bancaria-ar. Guiame, pero no operes mi banco, navegador, home banking, dinero ni reclamos externos por mí.

## MCP

MCP **no es la skill**. Agrega fuentes/herramientas.

Separación:
- Skill = criterio y protocolo.
- MCP = investigación jurídica read-only opcional.
- Humano = toda operación bancaria.

Ver [integrations.md](integrations.md).

## Instaladores del repo

`install/install.sh` y `install/install.ps1` instalan por defecto en `~/.agents/skills/cerrar-cuenta-bancaria-ar`, ruta útil para hosts que soportan ese alias.

Para Claude Code, pasar explícitamente el destino `~/.claude/skills/cerrar-cuenta-bancaria-ar`.

Los instaladores verifican que un checkout existente tenga el `origin` esperado antes de ejecutar `pull`, no sobrescriben una carpeta ajena y nunca solicitan credenciales bancarias. La validación local corre cuando Python está disponible.