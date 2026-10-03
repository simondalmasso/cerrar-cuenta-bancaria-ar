# cerrar-cuenta-bancaria-ar

Skill abierta, gratuita y vendor-neutral para que **cualquier agente de IA** guíe a una persona humana en el cierre de una cuenta bancaria en Argentina —banco público o privado— con normativa, evidencia, diagnóstico de bloqueos y escalamiento.

> **Aviso legal:** este proyecto es informativo y no constituye asesoramiento jurídico, financiero ni profesional. La IA guía; la persona decide y opera. Ver [DISCLAIMER.md](DISCLAIMER.md).

## Estado ejecutivo

| Control | Estado |
|---|---|
| Jurisdicción | Argentina |
| Scope principal | Personas humanas / usuarios de servicios financieros |
| Core runtime dependencies | **0** |
| Costo obligatorio | **USD 0** |
| Home banking / sesión autenticada | **Prohibido** |
| Operaciones de dinero | **Prohibidas** |
| Fuentes core | BCRA + Argentina.gob.ar + fuente oficial del banco |
| Integraciones externas | Opcionales y degradables |
| Eval suite | 45 especificaciones adversariales; no certificación conductual |
| Manifest | v1.2.0-dev (unreleased) |

### Ruta rápida

Si hubiera que presentar o revisar el proyecto en una hora, empezar por [docs/PRESENTATION.md](docs/PRESENTATION.md). Para investigación multi-motor y criterio de herramientas: [docs/RESEARCH-STACK.md](docs/RESEARCH-STACK.md).

### Release readiness

El estado machine-readable está en [registry/release-gate.json](registry/release-gate.json) y la explicación humana en [docs/RELEASE-GATE.md](docs/RELEASE-GATE.md). Mientras `behavioral-evals` siga `NOT_RUN`, **no** llamar estable a `1.2.0`.

### Documentos de auditoría

- [Executive audit](docs/EXECUTIVE-AUDIT.md)
- [Tooling audit / zero-cost review](docs/TOOLING-AUDIT.md)
- [Aviso legal](DISCLAIMER.md)
- [Modelo de seguridad](SECURITY.md)
- [Arquitectura](references/architecture.md)

## Qué hace

- identifica el tipo de cuenta y la regla aplicable;
- busca/contrasta fuentes oficiales actuales;
- detecta saldos, descubiertos, intereses, cheques y dependencias reales;
- evita loops de "volvé a pedir la baja";
- redacta frases para chat/llamada y reclamos;
- arma timeline y paquete de evidencia;
- escala banco → responsable de usuario → BCRA cuando corresponde;
- usa jurisprudencia oficial verificada solo si la controversia lo necesita.

## Modos de respuesta

- **FAST**: respuesta operativa corta.
- **LIVE**: frase inmediata para chat/llamada, antes de cualquier explicación.
- **FORENSIC**: expediente, fuentes, timeline, hipótesis y gaps.

El handoff mínimo entre agentes usa [registry/case-state.schema.json](registry/case-state.schema.json). Casos especiales y post-cierre están separados en referencias para no contaminar el flujo normal.

## Review playbook

En modo **FORENSIC**, la skill puede aplicar un checklist estructurado por etapas antes de escalar, cerrar o hacer un handoff crítico. Usa `SATISFIED / OPEN / NOT_APPLICABLE`, sin porcentajes de “cumplimiento jurídico”. Ver [references/review-playbook.md](references/review-playbook.md) y [registry/review-playbook.json](registry/review-playbook.json).

Este patrón fue incorporado como concepto después de revisar Prism Legal OS; no se agregó Prism como dependencia ni se copió su código.

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

Las releases de nivel superior fijadas declaran MIT en PyPI, pero sus repositorios fuente canónicos devolvieron 404 durante la auditoría del 2026-10-02. Por eso se clasifican como **OPTIONAL_PYPI / provenance_limited**, no como source auditado. Los SHA-256 del paquete de nivel superior están registrados; las dependencias transitivas siguen resolviéndose por rango salvo lock externo. Son aceleradores de investigación, **no fuentes bancarias ni actuadores**.

Ver [references/integrations.md](references/integrations.md). Hay un ejemplo combinado en [integrations/mcp-stdio.example.json](integrations/mcp-stdio.example.json).

**OpenArg / Vigía** quedan como discovery opcional: OpenArg para datasets públicos y Vigía para radar normativo. Ninguno reemplaza la fuente oficial ni es dependencia core.

## Web pública opcional

Para páginas oficiales difíciles de extraer, el repo acepta como adaptadores locales opcionales **Crawl4AI**, **Scrapy** y **Playwright en modo render-only**. No se instalan automáticamente y nunca pueden reutilizar sesiones, cookies o credenciales bancarias.

Ver [references/public-web-research.md](references/public-web-research.md).

## Fuentes core

- BCRA — Protección de usuarios
- BCRA — Depósitos de ahorro/cuenta sueldo/especiales
- BCRA — Reglamentación de cuenta corriente
- BCRA — Reclamos
- Argentina.gob.ar — cierre de cuenta

Ver [references/sources-ar.md](references/sources-ar.md). Para controversias, [references/jurisprudencia.md](references/jurisprudencia.md) y el registro estructurado [registry/case-law.json](registry/case-law.json).

## Ejemplo y perfiles opcionales

El único ejemplo incluido es [examples/case-synthetic/](examples/case-synthetic/): completamente ficticio y sin datos de usuarios. El core no hardcodea bancos; [banks/profile.schema.json](banks/profile.schema.json) define cómo podrían agregarse perfiles públicos opcionales sin convertirlos en protagonistas.

## Instalación rápida

Con Git:

```bash
git clone https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git ~/.agents/skills/cerrar-cuenta-bancaria-ar
```

También hay instaladores conservadores: verifican `origin`, exigen `main`, rechazan cambios locales o commits ahead/divergentes y solo permiten fast-forward hasta `origin/main` antes de ejecutar el validator. Ejecutan validación local **cuando Python está disponible**:

- `install/install.sh`
- `install/install.ps1`

Ver [references/client-setup.md](references/client-setup.md).

## Calidad

`python scripts/validate_repo.py` valida estructura, referencias locales, JSON, provenance registry, handoff A–G, review playbook, legal-watch, ejemplos sintéticos, consistencia de versión, 45 especificaciones adversariales y secretos accidentales. **No ejecuta un modelo ni certifica conducta.** El mismo chequeo corre en GitHub Actions. Un workflow separado verifica disponibilidad/integridad de fuentes y artefactos fijados; no certifica vigencia jurídica.

## Diseño de seguridad

La regla principal es:

> **La IA guía; el humano opera.**

Eso permite usar la skill incluso en escenarios financieros sensibles sin delegar autenticación, movimientos o decisiones irreversibles.

## Estado

v1.2.0-dev — hardening posterior a auditoría adversarial; todavía **sin tag/release**. La próxima release debe fijar un tag inmutable sobre el commit aprobado.

Antes de usar una regla jurídica material, el agente debe volver a verificar la fuente oficial si dispone de acceso actualizado.