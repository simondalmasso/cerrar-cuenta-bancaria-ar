# Integraciones de investigación

Fecha de revisión: **2026-10-03**.

## Decisión arquitectónica

**Core = Agent Skill. MCP = opcional. API propia = no necesaria en v1.x.**

La skill debe seguir funcionando si mañana desaparecen todos los servicios de terceros.

Un MCP/API solo puede buscar normativa/jurisprudencia pública, recuperar documentos y ayudar a verificar fuentes. Nunca puede entrar al banco, manipular home banking, mover dinero ni presentar una baja/reclamo por el usuario.

## Tier A — core gratuito y estable

Sin integración: BCRA, Argentina.gob.ar, sitio oficial del banco, SAIJ/CSJN vía web cuando estén accesibles y los archivos de esta skill. Esta es la ruta canónica.

## Tier B — paquetes PyPI opcionales con provenance limitada

**No describir actualmente estos cuatro paquetes como "source auditado/open-source auditable".**

Al 2026-10-03:
- las releases fijadas siguen disponibles en PyPI;
- PyPI declara MIT y Python >=3.10;
- PyPI publica wheel/sdist y SHA-256;
- los repositorios canónicos `hernan-cc/<paquete>` publicados en metadata devolvieron **404** al verificarlos nuevamente el 2026-10-03.

Por eso se clasifican como `OPTIONAL_PYPI / provenance_limited`.

**Límite de pinning:** el pin y los hashes cubren el paquete de nivel superior publicado en PyPI. Sus dependencias transitivas (`mcp` y, para `juscaba-mcp`, `httpx`) se resuelven por rango y no quedan hash-pinneadas por el ejemplo `uvx`; no presentar este bundle como instalación totalmente reproducible.

| Paquete | Pin | Wheel SHA-256 | Source repo |
|---|---:|---|---|
| [`saij-mcp`](https://pypi.org/project/saij-mcp/0.3.0/) | 0.3.0 | `bac95044c4822854f119c446b0c9eb0895e23e293ab9ab59fbc5df63f0bd5f6b` | 404 verificado 2026-10-03 |
| [`csjn-mcp`](https://pypi.org/project/csjn-mcp/0.3.0/) | 0.3.0 | `be0f32d63d661159f6d71f1f815d3571f7833158489b399a539f691117058839` | 404 verificado 2026-10-03 |
| [`juba-mcp`](https://pypi.org/project/juba-mcp/0.3.0/) | 0.3.0 | `24d99aa7dbacefe397d306086df5231b5631aef50a82300d4c846a0efc509b95` | 404 verificado 2026-10-03 |
| [`juscaba-mcp`](https://pypi.org/project/juscaba-mcp/0.3.1/) | 0.3.1 | `032f0e377841139a459b2c7378d13e857e5f2770e7dcdd6895ef9a9634d6983e` | 404 verificado 2026-10-03 |

El registro conserva también los hashes de sdist: [registry/sources.json](../registry/sources.json).

Ejemplo fijado: [integrations/mcp-stdio.example.json](../integrations/mcp-stdio.example.json).

Política:
- nunca hard dependency;
- ejecutar solo la versión fijada del paquete de nivel superior;
- asumir que las dependencias transitivas siguen flotando salvo que el operador use un lock/hash set propio;
- verificar metadata/hashes antes de cambiar el pin;
- usar como discovery/recuperación y conservar enlace oficial;
- si reaparece el source repo, auditarlo antes de elevar confianza;
- si falla, degradar a web oficial.

## Tier C — útiles pero condicionados

### Probanza-ar/mcp-legal-ar
https://github.com/Probanza-ar/mcp-legal-ar

Repo activo observado en 2026; múltiples fuentes jurídicas argentinas; licencia dual con uso no comercial gratuito. No es dependencia universal.

### Jurídica
https://juridica.ar/desarrolladores

API/MCP con API key y free tier publicado. Es fallback: verificar plan antes de cada uso.

### Argentina Data MCP
https://github.com/abenassi/argentina-data-mcp

Útil para InfoLEG/Boletín Oficial/BCRA/feriados; no core por límites/licencia.

### FalloBot
https://fallobot.com/

La búsqueda manual gratuita puede servir como discovery. Su MCP no integra el bundle gratuito.

### OpenArg MCP
https://mcp.openarg.org/

Uso: **datos públicos argentinos**, no autoridad jurídica. Al 2026-10-02 publica un plan gratuito de 200 consultas de datos y 10 preguntas por mes, con API key. Puede ayudar a localizar series BCRA y datasets oficiales, pero toda conclusión material debe volver a la fuente oficial.

Clasificación: `CONDITIONAL_FREE_TIER / public_data_discovery`.

### Vigía · OpenArg
https://vigia.openarg.org/

Uso: **discovery regulatorio**. Indexa Boletín Oficial, InfoLEG, Congreso, BCRA y otras fuentes públicas. El buscador/feed público es gratuito y el código publicado por Colossus Lab declara MIT.

Clasificación: `OPTIONAL_PUBLIC_DISCOVERY`. Un resumen o índice de Vigía nunca reemplaza el texto oficial: seguir el enlace y verificar la fuente primaria.

### WolframResearch/skills — referencia de authoring y cómputo opcional
https://github.com/WolframResearch/skills

El repo oficial de WolframResearch declara licencia MIT y sigue el estándar abierto Agent Skills. Se integra aquí **solo como referencia arquitectónica/documental**, sin copiar código ni agregar dependencia runtime.

Patrones adoptables:
- skill autocontenida alrededor de `SKILL.md`;
- compatibilidad multi-cliente;
- progressive disclosure hacia `references/`;
- instrucciones explícitas de cuándo usar herramientas;
- verificación/test antes de declarar éxito.

Si el host ya dispone de Wolfram, puede usarse opcionalmente para **aritmética exacta, fechas y sanity checks cuantitativos**. Nunca es autoridad jurídica ni reemplaza BCRA/ley/banco.

Reglas:
- cero credenciales bancarias;
- no enviar identificadores completos;
- no hard dependency;
- no requisito para el camino USD 0;
- si Wolfram no está disponible, usar cálculo local/determinista.

## No integrar como core

- MetaJurídico: trial/pago y scope de expedientes.
- JurisprudenciaARG: suscripción.
- Psflores/Legal-MCP-Server-: prototipo/packaging inconsistente.
- CENDOJ: jurisdicción España.

## Source integrity vs vigencia jurídica

El workflow automático verifica disponibilidad, host final, content-type, marcador mínimo de contenido y metadata/hash de artefactos PyPI fijados.

**No certifica vigencia jurídica ni interpretación normativa.** Antes de formular una afirmación legal material, el agente debe volver a leer la fuente oficial aplicable.