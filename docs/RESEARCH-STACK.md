# Research stack — discovery sin contaminar el core

## Principio

El repositorio no debe depender del buscador que esté disponible hoy. Separar:

```text
discovery multi-motor → verificación primaria → síntesis local
```

Un resultado de búsqueda nunca se convierte en autoridad por aparecer en varios motores.

## Herramientas del host

| Herramienta | Uso recomendado | ¿Autoridad? | ¿Dependencia del repo? |
|---|---|---:|---:|
| Exa | discovery web amplio y búsqueda semántica | No | No |
| Parallel Search | búsqueda redundante con extractos | No | No |
| Agentic Search by Liner | discovery/triangulación; deep research si el host lo permite | No | No |
| Tavily | búsqueda, extract y crawl de páginas públicas | No | No |
| Undermind | doctrina y literatura académica; no índice primario de fallos | No | No |
| Powerset Research | investigación de repos/proyectos y actividad OSS | No | No |
| Data / OSINT connectors | datasets o verificación pública según el conector | No | No |

Para derecho argentino: usar estos motores para **encontrar** el antecedente y terminar en CSJN, SAIJ, JUBA, JURISTECA, Poder Judicial provincial u otra publicación oficial.

## Referencia de authoring y cálculo determinista

**WolframResearch/skills** (MIT) se usa como referencia de diseño, no como dependencia. Su repo oficial sigue el estándar Agent Skills y refuerza el patrón `SKILL.md` + referencias + guidance explícita de herramientas.

Si el host ya tiene Wolfram disponible, puede servir como calculador opcional para netos, fechas o sanity checks numéricos. No es fuente jurídica, no recibe credenciales y no forma parte del camino obligatorio USD 0.

## Adaptadores locales aceptados

La decisión del tooling audit se mantiene:

`fetch nativo → Crawl4AI / Scrapy → Playwright render-only`

- **Crawl4AI:** extracción local de páginas públicas complejas.
- **Scrapy:** crawling estático/determinista.
- **Playwright:** renderizado JS como último recurso, sin autenticación ni acciones transaccionales.

## Candidatos revisados pero no integrados

Firecrawl, GPT Researcher, Browser Use, DeerFlow, Scrapling, STORM, SpiderFoot, GoogleScraper, open-seo-mcp-skills y Agent-Reach pueden ser útiles en otros proyectos, pero aquí no justifican convertirse en dependencia core. Las razones recurrentes son duplicación del host, peso operativo, superficie de navegador/acciones, sesiones/cookies, licencia/costo o irrelevancia jurídica.

Ver el detalle en [TOOLING-AUDIT.md](TOOLING-AUDIT.md).

## Anti-colisión

Cuando haya varios motores:
1. emitir consultas equivalentes en 2–3 motores;
2. deduplicar por URL/caso;
3. priorizar fuente oficial;
4. si solo aparece una fuente secundaria, marcar `REFERENCE`;
5. no incorporar un fallo como `VERIFIED_OFFICIAL` hasta abrir una publicación judicial oficial;
6. registrar diferencia material para evitar analogías exageradas.

## Regla de costo

El core sigue funcionando sin ningún servicio externo. Los conectores del host se usan solo cuando ya están disponibles o cuando el operador decide conectarlos; nunca se convierten en requisito del repositorio.