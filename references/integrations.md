# Integraciones de investigación

Fecha de auditoría: **2026-10-02**.

## Arquitectura recomendada

**Core = Agent Skill. MCP = opcional. API propia = no necesaria por ahora.**

Razones:
- el flujo principal es criterio, investigación y guía humana, no automatización bancaria;
- el estándar Agent Skills es portable entre múltiples hosts;
- el MCP agrega fuentes jurídicas, pero no debe ser requisito;
- una API/endpoint propio crearía hosting, seguridad, costos y mantenimiento sin mejorar el cierre de la cuenta.

Si más adelante se crea un servicio, debería ser un **broker read-only de fuentes públicas**, nunca un operador bancario.

## Tier A — sin integración externa

Siempre disponible:
- SKILL.md;
- fuentes oficiales por web;
- usuario como operador humano.

Esta es la ruta canónica.

## Tier B — MCP jurídicos gratuitos/open-source, opcionales

### saij-mcp
- paquete: `saij-mcp`
- distribución observada: PyPI
- licencia declarada: MIT
- auth: no requerida
- objetivo: SAIJ
- última release observada: 0.3.0, 2026-02-17
- uso: discovery/verificación de legislación y jurisprudencia argentina.

Ejemplo MCP stdio genérico:
```json
{
  "mcpServers": {
    "saij": {
      "command": "uvx",
      "args": ["saij-mcp"]
    }
  }
}
```

### csjn-mcp
- paquete: `csjn-mcp`
- distribución: PyPI
- licencia: MIT
- auth: no requerida
- objetivo: sumarios CSJN
- última release observada: 0.3.0, 2026-02-17
- limitación: los sumarios no sustituyen la lectura/verificación del fallo completo.

### juba-mcp
- paquete: `juba-mcp`
- licencia: MIT
- auth: no requerida para la base pública
- objetivo: jurisprudencia bonaerense
- última release observada: 0.3.0, 2026-02-17

### juscaba-mcp
- paquete: `juscaba-mcp`
- licencia: MIT
- objetivo: JusCABA
- última release observada: 0.3.1, 2026-02-17
- esta skill no necesita funciones sobre expedientes; usar solo búsquedas públicas pertinentes.

### Política de uso
- no son hard dependencies;
- antes de usarlos, comprobar que el paquete sigue disponible;
- tratar la respuesta como índice/discovery;
- conservar enlace a la fuente oficial;
- si el conector falla, volver a web oficial sin degradar el flujo.

## Tier C — hub argentino, opcional con restricción de licencia

### Probanza-ar/mcp-legal-ar
https://github.com/Probanza-ar/mcp-legal-ar

Auditoría:
- repo activo observado en 2026;
- múltiples fuentes jurídicas argentinas;
- ejecución local/read-only declarada;
- licencia dual: gratuito para uso no comercial; uso comercial requiere licencia.

Por eso **no es dependencia universal** de esta skill. Puede recomendarse a usuarios no comerciales que acepten su licencia y necesiten un hub local.

Para esta skill, usar solo conectores públicos de legislación/jurisprudencia. No cargar credenciales de expedientes, PJN, MEV o EJE.

## Tier D — servicios con free tier, no core

### Jurídica
https://juridica.ar/desarrolladores

A fecha de auditoría:
- API y MCP;
- API key requerida;
- plan free: 100 requests/día;
- fuentes declaradas: SAIJ, CSJN, JUBA;
- el free tier puede cambiar.

Útil como fallback cómodo, pero no es "gratis garantizado para siempre" ni debe ser requisito.

## No integrar como dependencia

### Psflores/Legal-MCP-Server-
https://github.com/Psflores/Legal-MCP-Server-

Motivos:
- push observado en 2025-06;
- README contiene rutas/URLs de plantilla `tu-usuario`;
- metadata del repo no presenta licencia reconocida aunque el README diga MIT;
- parece más demostración/prototipo que fuente mantenida.

Puede estudiarse como ejemplo de arquitectura MCP, no como fuente jurídica de producción.

### Hernán Caravario — repos GitHub individuales
La guía pública de 2026 documenta `saij-mcp`, `juba-mcp`, `csjn-mcp` y `juscaba-mcp`, pero los repos GitHub enlazados devolvieron 404 durante esta auditoría. Los paquetes PyPI sí estaban disponibles. Por eso integrar por **nombre de paquete**, no por clone de GitHub, y verificar disponibilidad en cada uso.

### JurisprudenciaARG
Servicio útil, pero el acceso completo/MCP está asociado a suscripción. No es dependencia gratuita permanente.

### MetaJurídico
Prueba gratuita temporal y producto pago. Además está orientado a expedientes de estudios. No corresponde como core de una skill pública gratuita.

### FalloBot
Tiene plan gratuito de búsqueda, pero el MCP requiere plan Pro según su sitio. No integrar como MCP gratuito.

### CENDOJ / mcp-cendoj-sentencias
Es España. Técnicamente sólido y gratuito, pero fuera de jurisdicción para cierre de cuentas bancarias argentinas.

## Regla universal para cualquier host

Si el agente soporta Agent Skills:
1. cargar esta carpeta como skill;
2. activar por descripción o por nombre;
3. usar MCP jurídicos solo si ya están configurados.

Si no soporta Agent Skills:
1. cargar `SKILL.md` como instrucciones;
2. permitir lectura de `references/`;
3. mantener exactamente las invariantes de no operación bancaria.

Nunca exigir una empresa de IA específica.
