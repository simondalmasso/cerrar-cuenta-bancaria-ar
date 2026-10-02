# Arquitectura portable

## Decisión

La unidad principal es una **Agent Skill vendor-neutral**, no un bot.

```
Humano
  |
  v
Agente IA
  |
  +-- SKILL.md --------------> decisión y protocolo
  |
  +-- references/ -----------> normativa, árbol, evidencia, escalamiento
  |
  +-- web oficial -----------> BCRA / Argentina.gob.ar / banco
  |
  +-- MCP jurídico opcional -> SAIJ / CSJN / JUBA / JusCABA
  |
  X  home banking / app bancaria / movimiento de dinero
```

## Por qué no un MCP bancario

Un MCP que cierre cuentas, navegue home banking o mueva dinero:
- aumenta drásticamente el riesgo;
- exige credenciales/2FA;
- depende de interfaces privadas cambiantes;
- reduce portabilidad;
- contradice el objetivo de mantener a la persona en control.

Esta skill deliberadamente no lo implementa.

## Por qué no una API propia

La lógica esencial es conocimiento/procedimiento. Las fuentes normativas ya son públicas. Una API propia solo tendría valor si:
- cachea normativa con versionado;
- normaliza directorios de bancos;
- hace health checks;
- expone fuentes sin credenciales.

Eso puede ser fase 2, pero debe ser read-only.

## Interfaz conceptual para fuentes

Cualquier host puede mapear estas capacidades:

- `search_web(query)`
- `fetch_url(url)`
- `search_official_law(query)`
- `search_case_law(query)`
- `read_user_evidence(file_or_text)`

Todas son de lectura.

Capacidades explícitamente prohibidas:
- `bank_login`
- `click_homebanking`
- `transfer_funds`
- `pay_balance`
- `close_account`
- `submit_complaint`

La salida de la skill es una instrucción para el humano y un expediente de evidencia, no una mutación externa.

## Progressive disclosure

- metadata: activa la skill;
- SKILL.md: reglas y decisión;
- references: solo cuando la rama lo exige;
- integraciones: solo si el host dispone de ellas;
- jurisprudencia: solo en controversias.

Esto mantiene el contexto chico y portable.
