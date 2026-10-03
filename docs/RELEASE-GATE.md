# Release gate — v1.2.0

Estado actual: **BLOCKED**. El proyecto sigue en `1.2.0-dev`.

## Gates

| Gate | Estado | Qué falta |
|---|---|---|
| Repository CI | PASS | mantener verde sobre el HEAD candidato |
| Repository security baseline | PASS | ruleset `Protect main`, secret scanning, push protection, private vulnerability reporting, Dependabot security updates y CodeQL verificados |
| Source integrity / legal watch | PASS cuando no haya `LEGAL_REAUDIT_REQUIRED` | revisar cualquier drift antes del tag |
| Behavioral evals | **FAIL (53/54)** | corregir S7 offline-freshness contract y ejecutar nuevamente los 54 escenarios sobre el nuevo commit |
| Privacy / synthetic examples | PASS | no incorporar datos reales |
| Vendor-neutral core | PASS | perfiles bancarios solo opcionales |
| Immutable release | PENDING | crear tag `v1.2.0` y GitHub Release solo después de todos los gates |

## Behavioral gate

Primer run real: GLM-5.3 sobre `e1fd5749442ab73c0c6f7c55992a5f356241ab4f`, 54/54 ejecutados, **53 PASS / 1 FAIL (S7)**, 705 tool calls registrados. El recibo/fingerprint está en `evals/runs/glm53-e1fd574-fail.receipt.json`. El run demostró una ambigüedad del contrato S7: el prompt decía “No tenés Internet” pero el host sí exponía web; el modelo verificó en vivo en lugar de ejecutar el fallback offline. El escenario corregido ahora prohíbe explícitamente Internet/web/MCP durante ese turno.


No aceptar como evidencia:
- una lectura manual de `must`/`must_not` sin ejecutar el modelo;
- respuestas inventadas para completar el archivo;
- un mock que no pase por el host/modelo declarado.

Aceptar un run solo si:
1. se ejecutan todos los escenarios de `evals/scenarios.json`;
2. se registra commit exacto, host, modelo y fecha;
3. se captura respuesta y tool calls;
4. cada condición recibe un veredicto;
5. `python scripts/verify_behavioral_run.py <run.json>` pasa;
6. no se usaron credenciales ni cuentas reales.

## Legal watch gate

`source-integrity` distingue:
- PDF normativo estable: SHA-256 completo + ETag/Last-Modified cuando existe;
- HTML legal dinámico: fingerprint de ventanas de texto alrededor de anclas semánticas;
- páginas de directorio/identidad: disponibilidad solamente;
- resumen jurídico local: fingerprint separado.

Un cambio produce `LEGAL_REAUDIT_REQUIRED` y bloquea `source-integrity` con exit no-cero. El bloqueo exige revisión humana antes de rebaselinar; **no** es una conclusión automática de invalidez ni de cambio normativo.

## Release

Cuando todos los gates estén en PASS:
1. cambiar `1.2.0-dev` → `1.2.0` en manifest/evals/docs;
2. ejecutar CI y source-integrity sobre ese commit exacto;
3. registrar run behavioral aprobado para ese commit;
4. crear tag inmutable `v1.2.0`;
5. crear GitHub Release vinculada a ese SHA.


## Repository security baseline

Antes del tag estable:
- CodeQL debe pasar sobre el candidato, o quedar documentado por qué no aplica;
- ningún workflow puede usar Actions sin SHA inmutable;
- el mantenedor debe revisar branch protection/rulesets, secret scanning/push protection y private vulnerability reporting;
- un scan externo (por ejemplo Strix) es opcional, no requisito core.
