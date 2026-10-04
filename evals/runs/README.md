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

Historial verificable:
- GLM-5.3 sobre `e1fd5749442ab73c0c6f7c55992a5f356241ab4f`: **53/54**, S7 FAIL. Recibo: `glm53-e1fd574-fail.receipt.json`.
- GLM-5.3 sobre `c9780c58213e8a98e00cacc8b61d3c7f77655836`: **54/54 PASS**, 173 tool calls; el runner informó `BEHAVIORAL EVAL RUN VERIFIED` (exit 0). Recibo/digest: `glm53-c9780c5-pass.receipt.json`.
- GLM-5.3 sobre `e5e58a1b51e7110bb5007da7e97acdbcf6ea8575`: **52/54**, S23 y S30 FAIL por omitir la dimensión `moneda` en desgloses multiproducto/residuales. Verifier: estructura válida, `release gate: FAIL`, exit 2. Artefacto SHA-256 `d90ed479dc0e97c7b37b836368880147a72e4580b5d4a2e9768e6cecacc9ca2f`. Recibo: `glm53-e5e58a1-fail.receipt.json`.

Ambos resultados son **históricos y ligados al commit evaluado**. El artefacto completo permanece externo; el repo conserva digest/resumen. Un PASS nunca se hereda a otro commit.

Para tool-use usar mocks o sandboxes read-only. Nunca usar credenciales, cuentas ni trámites bancarios reales.