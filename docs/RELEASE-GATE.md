# Criterios de publicación — v1.2.0

Estado actual: **BLOCKED**. El proyecto sigue en `1.2.0-dev`.

## Controles

| Control | Estado | Qué falta |
|---|---|---|
| CI del repositorio | PASS | mantener verde sobre el HEAD candidato |
| Seguridad del repositorio | PASS | ruleset `Protect main`, secret scanning, push protection, private vulnerability reporting, Dependabot security updates y CodeQL verificados |
| Integridad de fuentes / vigilancia legal | PASS cuando no haya `LEGAL_REAUDIT_REQUIRED` | revisar cualquier drift antes del tag |
| Evaluaciones conductuales | **NOT RUN (candidato actual)** | ejecutar S1–S54 completos contra el commit candidato exacto y conservar el artefacto verificable |
| Privacidad / ejemplos sintéticos | PASS | no incorporar datos reales |
| Núcleo independiente del proveedor | PASS | perfiles bancarios solo opcionales |
| Publicación inmutable | PENDING | crear tag `v1.2.0` y GitHub Release solo después de todos los gates |

## Evaluación conductual

El estado conductual siempre está ligado al commit exacto evaluado. Un `FAIL` pertenece al commit que falló; si el candidato cambia después, el nuevo candidato vuelve a `NOT_RUN` hasta su propio run completo. Un resultado histórico nunca se arrastra como estado actual.


### Evidencia histórica, no gate actual

GLM-5.3 ejecutó los 54 escenarios sobre el commit histórico `e1fd5749442ab73c0c6f7c55992a5f356241ab4f`: **53 PASS / 1 FAIL (S7)**, con 705 tool calls registrados. Ese run se conserva como evidencia de regresión en `evals/runs/glm53-e1fd574-fail.receipt.json`, pero **no define el estado del candidato actual** porque luego cambiaron `SKILL.md` y S7. Regla operativa: si cambia el comportamiento o el contrato de evals, el gate conductual vuelve a `NOT_RUN` hasta una ejecución completa sobre el nuevo commit.


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

## Vigilancia de fuentes jurídicas

`source-integrity` distingue:
- PDF normativo estable: SHA-256 completo + ETag/Last-Modified cuando existe;
- HTML legal dinámico: fingerprint de ventanas de texto alrededor de anclas semánticas;
- páginas de directorio/identidad: disponibilidad solamente;
- resumen jurídico local: fingerprint separado.

Un cambio produce `LEGAL_REAUDIT_REQUIRED` y bloquea `source-integrity` con exit no-cero. El bloqueo exige revisión humana antes de rebaselinar; **no** es una conclusión automática de invalidez ni de cambio normativo.

## Publicación

Cuando todos los gates estén en PASS:
1. cambiar `1.2.0-dev` → `1.2.0` en manifest/evals/docs;
2. ejecutar CI y source-integrity sobre ese commit exacto;
3. registrar run behavioral aprobado para ese commit;
4. crear tag inmutable `v1.2.0`;
5. crear GitHub Release vinculada a ese SHA.


## Seguridad del repositorio

Antes del tag estable:
- CodeQL debe pasar sobre el candidato, o quedar documentado por qué no aplica;
- ningún workflow puede usar Actions sin SHA inmutable;
- el mantenedor debe revisar branch protection/rulesets, secret scanning/push protection y private vulnerability reporting;
- un análisis externo (por ejemplo Strix) es opcional, no requisito del núcleo.
