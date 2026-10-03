# Adversarial eval specifications

`scenarios.json` contiene **43 especificaciones adversariales** de comportamiento esperado. No son, por sí solas, ejecuciones de un modelo.

`scripts/validate_repo.py` valida estructura:
- ID y nombre únicos;
- `prompt` no vacío;
- `must` no vacío;
- `must_not` no vacío;
- strings válidos.

El CI distingue explícitamente:
- **structure pass**;
- estado real del gate conductual leído desde `registry/release-gate.json`.

Mientras no exista un run real completo, el estado correcto es **NOT_RUN**.

## Runner por host

Cada proveedor/host puede convertir el mismo caso en una prueba conductual:

1. cargar la skill;
2. enviar `prompt`;
3. capturar respuesta y tool calls;
4. evaluar cada condición `must`;
5. evaluar cada prohibición `must_not`;
6. conservar modelo, versión, fecha y herramientas disponibles.

Un runner conductual no debe recibir credenciales bancarias reales ni operar servicios externos. Para casos de tool-use, usar mocks/sandboxes read-only.

El formato de evidencia está en `behavioral-run.schema.json`; los runs se guardan en `runs/` y se verifican con `python scripts/verify_behavioral_run.py <run.json>`. El verificador comprueba cobertura y consistencia, pero no inventa los juicios semánticos.

## Baseline jurídico

Los casos que contienen afirmaciones regulatorias se apoyan en `references/sources-ar.md`. Si cambia ese baseline, se deben revalidar las afirmaciones legales embebidas en los evals antes de una release.
