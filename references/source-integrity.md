# Source integrity protocol

Última revisión de política: **2026-10-02**.

Este protocolo separa **integridad técnica** de **vigencia jurídica**.

## Qué controla automáticamente

Para fuentes CORE oficiales:
1. HTTP 2xx;
2. host final permitido;
3. path esperado;
4. Content-Type esperado;
5. marcador mínimo de contenido;
6. `legal-watch` según estrategia: SHA-256 completo para PDFs normativos estables, ventanas semánticas para HTML dinámico y disponibilidad para directorios;
7. fingerprint del resumen jurídico local (`local_claim`).

Para paquetes PyPI opcionales fijados:
1. versión;
2. licencia declarada;
3. `requires_python`;
4. `requires_dist` esperado;
5. URL canónica declarada;
6. wheel + sdist por SHA-256;
7. estado `yanked` de cada artefacto.

## Qué NO certifica

Un resultado verde **no prueba** que:
- una norma siga jurídicamente vigente;
- la interpretación jurídica sea correcta;
- una modificación textual sea jurídicamente material o inmaterial.

Si cambia un fingerprint observado, el workflow emite `LEGAL_REAUDIT_REQUIRED`. Eso obliga a revisar la fuente y el resumen jurídico antes de rebaselinar; no declara por sí solo que la regla haya cambiado.

Antes de una afirmación jurídica material, el agente debe volver a leer la fuente oficial aplicable.

## Clasificación

- **CORE**: fuente oficial pública.
- **OPTIONAL_FREE**: helper gratuito/open-source reemplazable.
- **CONDITIONAL**: free tier, autenticación o licencia condicionada; verificar cada uso.
- **EXCLUDED_CORE**: pago/trial/jurisdicción incorrecta/stale/riesgo operativo.

Si una integración opcional falla, degradar a BCRA, Argentina.gob.ar, sitio oficial del banco y fuentes judiciales oficiales.

## Revisión manual

Los links de documentación de proveedores/hosts que puedan bloquear bots se revisan manualmente al menos en cada release y, si no hay release, trimestralmente. Un 403 de bot no se interpreta automáticamente como caída del recurso.

## Registro de vigilancia

`registry/legal-watch.json` guarda `checked_at`, sección relevante, estrategia, anclas semánticas cuando corresponden y fingerprints esperados. No editar un baseline solo para silenciar una alerta: primero verificar la fuente oficial y actualizar `references/sources-ar.md` si cambió la proposición jurídica.

## Gate de release

Para una release estable, `source-integrity` debe terminar sin `LEGAL_REAUDIT_REQUIRED` sobre el árbol candidato. El baseline técnico actual se declara en `registry/legal-watch.json`; cualquier rebaseline debe seguir a una revisión humana de la fuente oficial, no precederla.
