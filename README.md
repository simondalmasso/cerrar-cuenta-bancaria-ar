# cerrar-cuenta-bancaria-ar

Agent Skill abierta e independiente del proveedor para guiar a personas humanas en el cierre de cuentas bancarias en Argentina. Contrasta fuentes oficiales, diagnostica bloqueos, prepara mensajes y reclamos, y organiza evidencia; **la IA guía y la persona opera**.

> **Aviso legal:** proyecto informativo. No constituye asesoramiento jurídico, financiero ni profesional. Ver [DISCLAIMER.md](DISCLAIMER.md).

## Resumen

| Control | Estado |
|---|---|
| Jurisdicción | Argentina |
| Alcance | Personas humanas / usuarios de servicios financieros |
| Dependencias obligatorias del núcleo | **0** |
| Costo obligatorio | **USD 0** |
| Operaciones bancarias/autenticadas por IA | **Prohibidas** |
| Fuentes principales | BCRA + Argentina.gob.ar + sitio oficial del banco |
| Integraciones externas | Opcionales y degradables |
| Evaluaciones | 58 escenarios adversariales + contrato/verificador; ejecución completa del candidato actual pendiente |
| Versión | **1.2.0** — candidato final, sin tag/release estable todavía |

### Ruta de revisión

- [Guía de presentación y arquitectura](docs/PRESENTATION.md)
- [Estado de publicación](docs/RELEASE-GATE.md)
- [Política de investigación y herramientas](docs/RESEARCH-STACK.md)

### Estado de publicación

El estado del candidato está en [registry/release-gate.json](registry/release-gate.json). El candidato final requiere un run conductual completo S1–S58 sobre su commit exacto; hasta entonces no corresponde crear el tag/release `v1.2.0`. Tras un PASS final no se hacen más commits: la atestación definitiva se publica en el tag anotado/GitHub Release para no cambiar el SHA evaluado.

### Documentos de auditoría

- [Auditoría ejecutiva](docs/EXECUTIVE-AUDIT.md)
- [Respuesta a auditoría Arena — histórico](docs/ARENA-AUDIT-RESPONSE.md)
- [Respuesta a auditoría Gemini — histórico](docs/GEMINI-AUDIT-RESPONSE.md)
- [Auditoría de herramientas / costo cero](docs/TOOLING-AUDIT.md)
- [Aviso legal](DISCLAIMER.md)
- [Modelo de seguridad](SECURITY.md)
- [Arquitectura](references/architecture.md)

## Qué hace

- identifica el tipo de cuenta y la regla aplicable;
- busca/contrasta fuentes oficiales actuales;
- detecta saldos, descubiertos, intereses, cheques y dependencias reales;
- evita loops de "volvé a pedir la baja";
- redacta frases para chat/llamada y reclamos;
- arma una cronología y un paquete de evidencia;
- escala banco → responsable de usuario → BCRA cuando corresponde;
- usa jurisprudencia oficial verificada solo si la controversia lo necesita.

## Modos de respuesta

- **FAST**: respuesta operativa corta.
- **LIVE**: frase inmediata para chat/llamada, antes de cualquier explicación.
- **FORENSIC**: expediente, fuentes, cronología, hipótesis y faltantes.

El handoff mínimo entre agentes usa [registry/case-state.schema.json](registry/case-state.schema.json). Casos especiales y post-cierre están separados en referencias para no contaminar el flujo normal.

## Checklist de revisión FORENSIC

En modo **FORENSIC**, la skill puede aplicar un checklist estructurado por etapas antes de escalar, cerrar o hacer un handoff crítico. Usa `SATISFIED / OPEN / NOT_APPLICABLE`, sin porcentajes de “cumplimiento jurídico”. Ver [references/review-playbook.md](references/review-playbook.md) y [registry/review-playbook.json](registry/review-playbook.json).

Este patrón fue incorporado como concepto después de revisar Prism Legal OS; no se agregó Prism como dependencia ni se copió su código.

## Qué NO hace

**No toca el banco.** Puede consultar web pública oficial en modo lectura. No controla una sesión autenticada, home banking o app bancaria; no mueve dinero, no paga saldos, no cierra productos, no envía formularios y no recibe claves/token.

La persona mantiene el control de cada acción externa.

## Arquitectura

El núcleo es una **Agent Skill**, no un bot, API ni MCP.

```
Agente IA
  ├─ SKILL.md
  ├─ references/       normativa + decisión + evidencia
  ├─ assets/templates/ textos reutilizables
  └─ MCP opcional      solo investigación jurídica en lectura
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

Ver [references/client-setup.md](references/client-setup.md) para rutas comunes de instalación sin duplicar la skill por proveedor. El archivo opcional `agents/openai.yaml` agrega presentación nativa para OpenAI sin cambiar el núcleo independiente del proveedor.

## MCP: opcional

La skill funciona sin MCP. Para investigación jurídica puede usar paquetes PyPI opcionales, fijados por versión y con procedencia limitada documentada:

- [`saij-mcp`](https://pypi.org/project/saij-mcp/0.3.0/)
- [`csjn-mcp`](https://pypi.org/project/csjn-mcp/0.3.0/)
- [`juba-mcp`](https://pypi.org/project/juba-mcp/0.3.0/)
- [`juscaba-mcp`](https://pypi.org/project/juscaba-mcp/0.3.1/)

Las releases de nivel superior fijadas declaran MIT en PyPI, pero sus repositorios fuente canónicos seguían devolviendo 404 al verificarlos el 2026-10-03. Por eso se clasifican como **OPTIONAL_PYPI / provenance_limited**, no como código fuente auditado. Los SHA-256 del paquete de nivel superior están registrados; las dependencias transitivas siguen resolviéndose por rango salvo lock externo. Son aceleradores de investigación, **no fuentes bancarias ni actuadores**.

Ver [references/integrations.md](references/integrations.md). Hay un ejemplo combinado en [integrations/mcp-stdio.example.json](integrations/mcp-stdio.example.json).

**OpenArg / Vigía** quedan como descubrimiento opcional: OpenArg para datos públicos y Vigía para radar normativo. Ninguno reemplaza la fuente oficial ni es dependencia del núcleo.

## Web pública opcional

Para páginas oficiales difíciles de extraer, el repo acepta como adaptadores locales opcionales **Crawl4AI**, **Scrapy** y **Playwright en modo render-only**. No se instalan automáticamente y nunca pueden reutilizar sesiones, cookies o credenciales bancarias.

Ver [references/public-web-research.md](references/public-web-research.md).

## Fuentes principales

- BCRA — Protección de usuarios
- BCRA — Depósitos de ahorro/cuenta sueldo/especiales
- BCRA — Reglamentación de cuenta corriente
- BCRA — Reclamos
- Argentina.gob.ar — cierre de cuenta

Ver [references/sources-ar.md](references/sources-ar.md). Para controversias, [references/jurisprudencia.md](references/jurisprudencia.md) y el registro estructurado [registry/case-law.json](registry/case-law.json).

## Ejemplo y perfiles opcionales

El único ejemplo incluido es [examples/case-synthetic/](examples/case-synthetic/): completamente ficticio y sin datos de usuarios. El núcleo no fija bancos concretos; [banks/profile.schema.json](banks/profile.schema.json) define cómo podrían agregarse perfiles públicos opcionales sin convertirlos en protagonistas.

## Instalación rápida

Con Git:

```bash
git clone https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git ~/.agents/skills/cerrar-cuenta-bancaria-ar
```

También hay instaladores conservadores: verifican `origin`, exigen `main`, rechazan cambios locales o commits ahead/divergentes y solo permiten fast-forward hasta `origin/main` antes de ejecutar el validator. Ejecutan validación local **cuando Python está disponible**:

- `install/install.sh`
- `install/install.ps1`

Ver [references/client-setup.md](references/client-setup.md).

## Seguridad del repositorio

Además de la seguridad bancaria, el repo aplica controles de cadena de suministro: Dependabot para GitHub Actions, CodeQL para Python y validación de que toda Action esté fijada a un SHA inmutable. Ver [docs/SECURITY-HARDENING.md](docs/SECURITY-HARDENING.md).

`gh-secure` queda como herramienta opcional del mantenedor para revisar settings de GitHub. Strix queda como assurance externo opcional; sus scans no son dependencia core y requieren autorización explícita.

## Calidad

`python scripts/validate_repo.py` valida estructura, referencias locales, JSON, registro de procedencia, handoff A–G, review playbook, legal-watch, ejemplos sintéticos, consistencia de versión, 58 escenarios adversariales y secretos accidentales. **No ejecuta un modelo ni certifica conducta.** El mismo chequeo corre en GitHub Actions. Un workflow separado verifica disponibilidad/integridad de fuentes y artefactos fijados; no certifica vigencia jurídica.

## Diseño de seguridad

La regla principal es:

> **La IA guía; el humano opera.**

Eso permite usar la skill incluso en escenarios financieros sensibles sin delegar autenticación, movimientos o decisiones irreversibles.

## Estado

**1.2.0** — candidato final en validación. No existe todavía un tag/release estable; `v1.2.0` solo se publica cuando todos los gates del candidato exacto estén en PASS.

Antes de usar una regla jurídica material, el agente debe volver a verificar la fuente oficial si dispone de acceso actualizado.