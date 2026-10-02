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

**No toca el banco.** Puede consultar web pública oficial en modo lectura. No controla una sesión autenticada, home banking o app bancaria; no mueve dinero, no paga saldos, no cierra productos, no envía formularios y no recibe claves/token.

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

## Conexión por agente

Ver [references/client-setup.md](references/client-setup.md) para rutas comunes de instalación sin duplicar la skill por proveedor. El archivo opcional `agents/openai.yaml` agrega presentación nativa para OpenAI sin cambiar el core vendor-neutral.

## MCP: opcional

La skill funciona sin MCP. Para investigación jurídica puede usar paquetes PyPI opcionales y fijados por versión cuando estén disponibles:

- `saij-mcp`
- `csjn-mcp`
- `juba-mcp`
- `juscaba-mcp`

Las releases fijadas declaran MIT en PyPI, pero sus repositorios fuente canónicos devolvieron 404 durante la auditoría del 2026-10-02. Por eso se clasifican como **OPTIONAL_PYPI / provenance_limited**, no como source auditado. Los SHA-256 están registrados. Son aceleradores de investigación, **no fuentes bancarias ni actuadores**.

Ver [references/integrations.md](references/integrations.md). Hay un ejemplo combinado en [integrations/mcp-stdio.example.json](integrations/mcp-stdio.example.json).

## Fuentes core

- BCRA — Protección de usuarios
- BCRA — Depósitos de ahorro/cuenta sueldo/especiales
- BCRA — Reglamentación de cuenta corriente
- BCRA — Reclamos
- Argentina.gob.ar — cierre de cuenta

Ver [references/sources-ar.md](references/sources-ar.md).

## Instalación rápida

Con Git:

```bash
git clone https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git ~/.agents/skills/cerrar-cuenta-bancaria-ar
```

También hay instaladores conservadores que verifican el `origin` antes de actualizar y **no pisan** una carpeta ajena. Ejecutan validación local **cuando Python está disponible**:

- `install/install.sh`
- `install/install.ps1`

Ver [references/client-setup.md](references/client-setup.md).

## Calidad

`python scripts/validate_repo.py` valida estructura, referencias locales, JSON, provenance registry, 22 especificaciones adversariales y secretos accidentales. **No ejecuta un modelo ni certifica conducta.** El mismo chequeo corre en GitHub Actions. Un workflow separado verifica disponibilidad/integridad de fuentes y artefactos fijados; no certifica vigencia jurídica.

## Diseño de seguridad

La regla principal es:

> **La IA guía; el humano opera.**

Eso permite usar la skill incluso en escenarios financieros sensibles sin delegar autenticación, movimientos o decisiones irreversibles.

## Estado

v1.1.1 — hardening de provenance/pinning, source-integrity, instaladores, prompt-injection, CI por SHA y 22 especificaciones adversariales.

Antes de usar una regla jurídica material, el agente debe volver a verificar la fuente oficial si dispone de acceso actualizado.