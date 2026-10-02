# cerrar-cuenta-bancaria-ar

Skill abierta, gratuita y vendor-neutral para que **cualquier agente de IA** guíe a una persona humana en el cierre de una cuenta bancaria en Argentina —banco público o privado— con normativa, evidencia, diagnóstico de bloqueos y escalamiento.

## Qué hace

- identifica el tipo de cuenta y la regla aplicable;
- busca/contrasta fuentes oficiales actuales;
- detecta saldos, descubiertos, intereses, cheques y dependencias reales;
- evita loops de "volvé a pedir la baja";
- redacta frases para chat/llamada y reclamos;
- arma timeline y paquete de evidencia;
- escala banco → responsable de usuario → BCRA cuando corresponde;
- usa jurisprudencia solo si la controversia lo necesita.

## Qué NO hace

**No toca el banco.** No navega home banking, no usa el mouse del usuario, no inicia sesión, no mueve dinero, no paga saldos, no cierra productos, no envía formularios y no recibe claves/token.

La persona mantiene el control de cada acción externa.

## Arquitectura

El core es un **Agent Skill**, no un bot, API ni MCP.

```
Agente IA
  ├─ SKILL.md
  ├─ references/       normativa + decisión + evidencia
  ├─ assets/templates/ textos reutilizables
  └─ MCP opcional      solo investigación jurídica read-only
```

Esto evita atar el proyecto a OpenAI, Anthropic, Google u otra empresa.

## Conexión

La skill sigue el estándar abierto de Agent Skills: una carpeta con `SKILL.md`.

### Opción neutral

Cloná el repo dentro del directorio de skills que soporte tu agente. Los clientes que soportan el estándar abierto pueden leer la misma carpeta sin modificar su contenido.

Ejemplo de estructura:

```
.agents/
  skills/
    cerrar-cuenta-bancaria-ar/
      SKILL.md
      references/
      assets/
```

Si tu agente usa otra ruta (`.claude/skills`, `.gemini/skills`, etc.), apuntá esa ruta a la misma carpeta o copiá el paquete. No mantengas versiones distintas del contenido.

### Agente sin soporte nativo de Skills

Cargá `SKILL.md` como instrucción y permitile leer `references/`. La lógica no depende de herramientas propietarias.

## MCP: opcional

La skill funciona sin MCP. Para investigación jurídica puede usar conectores gratuitos/open-source cuando estén disponibles:

- `saij-mcp`
- `csjn-mcp`
- `juba-mcp`
- `juscaba-mcp`

Se auditaron como paquetes PyPI gratuitos/MIT al 2026-10-02. Son aceleradores de investigación, **no fuentes bancarias ni actuadores**.

Ver [references/integrations.md](references/integrations.md).

## Fuentes core

- BCRA — Protección de usuarios
- BCRA — Depósitos de ahorro/cuenta sueldo/especiales
- BCRA — Reglamentación de cuenta corriente
- BCRA — Reclamos
- Argentina.gob.ar — cierre de cuenta

Ver [references/sources-ar.md](references/sources-ar.md).

## Diseño de seguridad

La regla principal es:

> **La IA guía; el humano opera.**

Eso permite usar la skill incluso en escenarios financieros sensibles sin delegar autenticación, movimientos o decisiones irreversibles.

## Estado

v1.0.0 — arquitectura, protocolo, fuentes, integraciones auditadas, templates y 10 familias de evaluación.

Antes de usar una regla jurídica material, el agente debe volver a verificar la fuente oficial si dispone de acceso actualizado.
