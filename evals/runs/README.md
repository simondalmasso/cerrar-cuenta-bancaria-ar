# Behavioral eval runs

Las especificaciones de `../scenarios.json` no certifican conducta hasta que un host/modelo real las ejecute.

## Contrato de evidencia

Un run real debe registrar:
- commit exacto de la skill;
- host y modelo;
- fecha;
- respuesta completa;
- tool calls;
- veredicto booleano para cada `must` y cada `must_not`;
- identidad del juez: humano, modelo o híbrido.

Validar con:

```bash
python scripts/verify_behavioral_run.py evals/runs/<archivo>.json
```

El repo **no** contiene un run ficticio de PASS. Hasta que exista un run real completo, el release gate mantiene `behavioral-evals = NOT_RUN`.

Para tool-use usar mocks o sandboxes read-only. Nunca usar credenciales, cuentas ni trámites bancarios reales.
