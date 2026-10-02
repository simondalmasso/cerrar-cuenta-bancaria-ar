# Integraciones de investigación

Fecha de auditoría: **2026-10-02**.

## Decisión arquitectónica

**Core = Agent Skill. MCP = opcional. API propia = no necesaria en v1.x.**

La skill debe seguir funcionando si mañana desaparecen todos los servicios de terceros.

Un MCP/API solo puede:
- buscar normativa/jurisprudencia pública;
- recuperar documentos;
- ayudar a verificar fuentes.

Nunca puede:
- entrar al banco;
- manipular home banking;
- mover dinero;
- presentar una baja o reclamo por el usuario.

## Tier A — core gratuito y estable

Sin integración:
- BCRA;
- Argentina.gob.ar;
- sitio oficial del banco;
- SAIJ/CSJN vía web cuando estén accesibles;
- SKILL.md + references/.

Esta es la ruta canónica.

## Tier B — MCP argentinos open-source/gratuitos

### saij-mcp
- paquete PyPI: `saij-mcp`;
- versión observada: 0.3.0 (2026-02-17);
- licencia: MIT;
- Python >=3.10;
- sin API key;
- fuente: SAIJ.

### csjn-mcp
- paquete PyPI: `csjn-mcp`;
- versión observada: 0.3.0 (2026-02-17);
- licencia: MIT;
- sin API key;
- fuente: sumarios CSJN;
- límite conceptual: sumario != fallo completo.

### juba-mcp
- paquete PyPI: `juba-mcp`;
- versión observada: 0.3.0 (2026-02-17);
- licencia: MIT;
- sin API key;
- fuente: JUBA / Buenos Aires.

### juscaba-mcp
- paquete PyPI: `juscaba-mcp`;
- versión observada: 0.3.1 (2026-02-17);
- licencia: MIT;
- sin API key para búsqueda pública relevante;
- fuente: Justicia CABA.

Guía vigente observada:
https://hernancc.com/guia-mcp

Ejemplo:
[integrations/mcp-stdio.example.json](../integrations/mcp-stdio.example.json)

### Política
- opcionales, nunca hard dependency;
- verificar disponibilidad antes de instalar;
- usar como discovery/recuperación;
- conservar enlace oficial;
- si falla, volver a fuentes oficiales web.

## Tier C — útiles pero condicionados

### Probanza-ar/mcp-legal-ar
https://github.com/Probanza-ar/mcp-legal-ar

Observado:
- repo activo en 2026;
- integra SAIJ, CSJN, InfoLEG, BORA y otras fuentes;
- ejecución local/read-only declarada para fuentes públicas;
- licencia dual: uso no comercial gratuito; uso comercial requiere licencia.

Uso permitido en esta arquitectura:
- solo investigación pública;
- nunca credenciales PJN/MEV/EJE para este caso;
- no hacerlo dependencia universal por su licencia.

### Jurídica
https://juridica.ar/desarrolladores

Observado el 2026-10-02:
- API REST + MCP;
- SAIJ, CSJN y JUBA;
- API key requerida;
- plan free publicado: **100 requests/día**;
- endpoint MCP publicado: `https://juridica.ar/mcp`.

Es un fallback práctico. El free tier es política comercial y puede cambiar: verificar antes de usar.

### Argentina Data MCP
https://github.com/abenassi/argentina-data-mcp

Aporta:
- `infoleg_search`;
- Boletín Oficial;
- datos BCRA generales;
- cálculo/consulta de feriados útil para plazos.

Observado:
- hosted free tier: 20 consultas/día;
- repo abierto y auditable;
- licencia PolyForm Noncommercial 1.0.0 para uso local.

No es dependencia core por límites/licencia. Útil como fallback de InfoLEG o para contar días hábiles.

### FalloBot — solo búsqueda manual gratuita
https://fallobot.com/

Observado el 2026-10-02:
- plan Free anunciado como "Gratis para siempre";
- 1 investigación IA/día;
- 5 búsquedas/día;
- fuentes públicas;
- **MCP requiere plan Pro**.

Conclusión: puede usarse como discovery manual gratuito cuando convenga; no integrar su MCP en el bundle gratuito.

## No integrar como core

### MetaJurídico
https://metajuridico.com/mcp-ia-abogados/

- trial 14 días;
- después requiere plan;
- orientado a datos/expedientes de estudios y acciones;
- no es un recurso gratuito permanente ni necesario para una baja bancaria.

### JurisprudenciaARG
https://www.cpacf.org.ar/noticia/convenios-y-beneficios/101/jurisprudenciaarg

- producto por suscripción;
- ofrece MCP y monitoreo;
- CPACF publica beneficio/descuento, no gratuidad permanente.

### Psflores/Legal-MCP-Server-
https://github.com/Psflores/Legal-MCP-Server-

- último push observado: 2025-06;
- README mantiene placeholders `tu-usuario`;
- metadata GitHub no expone licencia reconocida aunque README declara MIT;
- útil como ejemplo, no como dependencia productiva.

### CENDOJ / mcp-cendoj-sentencias
- gratuito/MIT y activo;
- jurisdicción España;
- fuera de alcance para cierre de cuentas argentinas.

## Regla de frescura

Antes de recomendar cualquier integración:
1. comprobar que sigue accesible;
2. comprobar licencia;
3. comprobar si requiere pago/API key;
4. comprobar última actividad o release;
5. si cambió, degradar a otra fuente sin afectar el workflow.

El archivo [registry/sources.json](../registry/sources.json) resume el estado auditado.
