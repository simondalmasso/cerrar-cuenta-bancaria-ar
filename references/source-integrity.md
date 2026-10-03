# Source integrity protocol

Última revisión de política: **2026-10-02**.

Este protocolo separa **integridad técnica** de **vigencia jurídica**.

## Qué controla automáticamente

Para fuentes CORE oficiales:
1. HTTP 2xx;
2. host final permitido;
3. path esperado;
4. Content-Type esperado;
5. marcador mínimo de contenido.

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
- un PDF oficial no haya cambiado de contenido manteniendo la misma URL.

Antes de una afirmación jurídica material, el agente debe volver a leer la fuente oficial aplicable.

## Clasificación

- **CORE**: fuente oficial pública.
- **OPTIONAL_FREE**: helper gratuito/open-source reemplazable.
- **CONDITIONAL**: free tier, autenticación o licencia condicionada; verificar cada uso.
- **EXCLUDED_CORE**: pago/trial/jurisdicción incorrecta/stale/riesgo operativo.

Si una integración opcional falla, degradar a BCRA, Argentina.gob.ar, sitio oficial del banco y fuentes judiciales oficiales.

## Revisión manual

Los links de documentación de proveedores/hosts que puedan bloquear bots se revisan manualmente al menos en cada release y, si no hay release, trimestralmente. Un 403 de bot no se interpreta automáticamente como caída del recurso.
