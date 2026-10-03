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


### Runs históricos

Los runs de commits anteriores se conservan únicamente como evidencia de regresión en [../evals/runs/](../evals/runs/). No definen el gate del candidato actual. Si cambia la skill, el contrato de evals o cualquier comportamiento relevante, `behavioral-evals` vuelve a `NOT_RUN` hasta una ejecución completa sobre el nuevo commit.


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

La configuración administrativa ya está verificada y en PASS: ruleset de `main`, secret scanning, push protection, private vulnerability reporting y Dependabot security updates. Para cada candidato de release, `validate` y CodeQL deben seguir verdes sobre el SHA exacto.

Un análisis externo adicional (por ejemplo Strix) es opcional y no forma parte del gate obligatorio.
