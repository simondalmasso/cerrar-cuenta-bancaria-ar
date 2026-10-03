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

El repo **no** contiene un run ficticio de PASS. Un run real puede cerrar `NOT_RUN` y aun así dejar el gate en `FAIL`; solo 54/54 permite `PASS`.

El primer run real completo fue GLM-5.3 sobre `e1fd5749442ab73c0c6f7c55992a5f356241ab4f`: 53/54, con fallo S7. El repo conserva un recibo/fingerprint en `glm53-e1fd574-fail.receipt.json`; el JSON completo se mantiene como artefacto externo y su SHA-256 permite verificar identidad.

Para tool-use usar mocks o sandboxes read-only. Nunca usar credenciales, cuentas ni trámites bancarios reales.
