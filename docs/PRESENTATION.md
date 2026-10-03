# Presentation pack — revisión en una hora

Este documento es la ruta corta para revisar o presentar el proyecto sin recorrer todo el repositorio.

## 60 segundos

**Problema:** cerrar una cuenta bancaria argentina puede entrar en loops por saldos, productos vinculados, cargos residuales, requisitos mal explicados o derivaciones contradictorias.

**Producto:** una Agent Skill vendor-neutral que investiga la regla aplicable, clasifica el caso, prepara la acción humana mínima, conserva evidencia y escala cuando corresponde.

**Límite deliberado:** la IA no entra al banco, no recibe credenciales, no mueve dinero y no presenta trámites por el usuario.

**Arquitectura:** core estático, cero dependencias obligatorias, fuentes oficiales primero, research/browser tooling opcional y read-only.

## Ruta de lectura — 10 minutos

1. [../README.md](../README.md) — alcance, estado y garantías.
2. [../SKILL.md](../SKILL.md) — comportamiento que recibe el agente.
3. [../references/decision-tree.md](../references/decision-tree.md) — lógica operativa.
4. [../references/sources-ar.md](../references/sources-ar.md) — baseline normativo.
5. [../references/jurisprudencia.md](../references/jurisprudencia.md) — controversias y antecedentes verificados.
6. [EXECUTIVE-AUDIT.md](EXECUTIVE-AUDIT.md) — assurance y riesgos.
7. [TOOLING-AUDIT.md](TOOLING-AUDIT.md) — por qué el core sigue en USD 0.
8. [RELEASE-GATE.md](RELEASE-GATE.md) — qué falta objetivamente para llamar estable a v1.2.0.
9. [ARENA-AUDIT-RESPONSE.md](ARENA-AUDIT-RESPONSE.md) — qué hallazgos externos fueron confirmados, corregidos o rechazados con evidencia.

## Demo de 5 minutos

Escenario recomendado:

> “Pedí la baja. El banco dijo que había una deuda. La pagué. Volví a pedirla y ahora me rechazan sin explicar por qué.”

La skill debería:
1. clasificar el producto y verificar si es cuenta corriente/depósito;
2. separar saldo, intereses, impuestos y cargos;
3. no asumir que el pago cerró automáticamente el blocker;
4. pedir causa exhaustiva y estado de la solicitud anterior;
5. evitar repetir indefinidamente la misma baja;
6. producir texto de reclamo y timeline;
7. escalar con evidencia si corresponde.

Esto muestra el valor diferencial: **diagnóstico + evidencia + próxima acción**, no automatización bancaria.

## Arquitectura para mostrar

```text
Fuentes oficiales ─────┐
                       ├─> Agent Skill ─> análisis ─> instrucción al humano
Jurisprudencia oficial ┤                    │
                       │                    X
Discovery opcional ────┘             sesión bancaria
```

El proyecto separa tres capas:
- **autoridad:** BCRA, Argentina.gob.ar, tribunales oficiales;
- **razonamiento:** SKILL + referencias + árbol de decisión;
- **transporte/discovery:** fetch nativo, Crawl4AI/Scrapy/Playwright o buscadores del host.

## Controles que importan

- `0` dependencias runtime obligatorias.
- `USD 0` de costo obligatorio.
- sesiones bancarias autenticadas: prohibidas.
- secretos/OTP/PIN/CVV: prohibidos.
- 52 especificaciones adversariales estructurales.
- CI valida repositorio e instaladores.
- source-integrity controla fuentes oficiales y provenance PyPI.
- jurisprudencia incorporada solo desde publicación judicial oficial.

## Qué está probado y qué no

**Probado por CI:** estructura, JSON, links locales, provenance, parsers de instaladores, escenarios adversariales como especificaciones y batería real-Git del updater.

**No probado automáticamente:** que una norma siga jurídicamente vigente por el solo hecho de que la URL responda; que un modelo concreto cumpla conductualmente las 52 specs; que un banco cierre efectivamente el producto.

## Repo map

```text
SKILL.md                    comportamiento principal
references/                 conocimiento operativo y jurídico
  sources-ar.md             baseline BCRA/Gobierno
  decision-tree.md          ramas del caso
  jurisprudencia.md         cuándo usar fallos
registry/
  sources.json              fuentes/provenance
  legal-watch.json          fingerprints + re-audit trigger
  case-state.schema.json    handoff A–G / FAST-LIVE-FORENSIC
  review-playbook.json       stage gates FORENSIC sin score legal
  case-law.json             jurisprudencia verificada
  release-gate.json         estado de salida estable
  tooling.json              tooling opcional
assets/templates/           intake y guiones
evals/                      especificaciones adversariales
scripts/                    validación e integrity checks
docs/                       auditoría, tooling, research y presentación
install/                    instalación conservadora
```

## Preguntas difíciles esperables

**¿Por qué no automatiza el home banking?**  
Porque añadir acceso autenticado no mejora la calidad jurídica del diagnóstico y aumenta riesgo, superficie de secretos y posibilidad de acciones irreversibles.

**¿Por qué no meter diez frameworks de research?**  
Porque discovery no es autoridad. El proyecto prefiere redundancia a nivel host y mantiene el core sin dependencias. La fuente final vuelve a BCRA/tribunal oficial.

**¿La jurisprudencia convierte esto en asesoramiento legal?**  
No. Los fallos funcionan como antecedentes contextuales en controversias; la skill no promete resultado, no representa al usuario y no sustituye análisis profesional.

**¿Está listo para release?**  
No todavía. Está en `1.2.0-dev`: el gap explícito es ejecutar behavioral evals reales sobre un host/modelo y, recién con todos los gates verdes, crear tag/release inmutable.
