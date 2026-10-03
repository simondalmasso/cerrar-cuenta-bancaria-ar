# Release gate — v1.2.0

Estado actual: **BLOCKED**. El proyecto sigue en `1.2.0-dev`.

## Gates

| Gate | Estado | Qué falta |
|---|---|---|
| Repository CI | PASS | mantener verde sobre el HEAD candidato |
| Source integrity / legal watch | PASS cuando no haya `LEGAL_REAUDIT_REQUIRED` | revisar cualquier drift antes del tag |
| Behavioral evals | **NOT RUN** | ejecutar los 43 escenarios en un host/modelo real y guardar evidencia verificable |
| Privacy / synthetic examples | PASS | no incorporar datos reales |
| Vendor-neutral core | PASS | perfiles bancarios solo opcionales |
| Immutable release | PENDING | crear tag `v1.2.0` y GitHub Release solo después de todos los gates |

## Behavioral gate

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

Un cambio produce `LEGAL_REAUDIT_REQUIRED`; es **warning operativo**, no una conclusión automática de invalidez. Antes de una release estable debe quedar revisado y rebaselinedo conscientemente.

## Release

Cuando todos los gates estén en PASS:
1. cambiar `1.2.0-dev` → `1.2.0` en manifest/evals/docs;
2. ejecutar CI y source-integrity sobre ese commit exacto;
3. registrar run behavioral aprobado para ese commit;
4. crear tag inmutable `v1.2.0`;
5. crear GitHub Release vinculada a ese SHA.
