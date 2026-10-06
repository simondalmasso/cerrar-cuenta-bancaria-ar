# Adversarial eval specifications

`scenarios.json` contiene **58 especificaciones adversariales** de comportamiento esperado. No son, por sí solas, ejecuciones de un modelo.

`scripts/validate_repo.py` valida estructura:
- ID y nombre únicos;
- `prompt` no vacío;
- `must` no vacío;
- `must_not` no vacío;
- strings válidos.

El CI distingue explícitamente:
- **structure pass**;
- estado real del gate conductual leído desde `registry/release-gate.json`.

El estado se define **por commit candidato**. Para un commit sin run completo, el estado correcto es **NOT_RUN**. Si ese mismo commit tiene un run completo con uno o más fallos, es **FAIL**; si cambia el comportamiento o el contrato de evals después, el nuevo commit vuelve a **NOT_RUN** hasta su propio run completo.

## Runner por host

Cada proveedor/host puede convertir el mismo caso en una prueba conductual:

1. cargar la skill;
2. enviar `prompt`;
3. capturar respuesta y tool calls;
4. evaluar cada condición `must`;
5. evaluar cada prohibición `must_not`;
6. conservar modelo, versión, fecha y herramientas disponibles.

Si un escenario impone una **restricción explícita de herramientas** (por ejemplo, S7: no usar Internet/web/MCP), el runner debe respetarla aunque el host técnicamente tenga esas herramientas. La restricción forma parte del escenario; no debe reinterpretarse como una afirmación factual a refutar.

Un runner conductual no debe recibir credenciales bancarias reales ni operar servicios externos. Para casos de tool-use, usar mocks/sandboxes read-only.

El formato de evidencia está en `behavioral-run.schema.json`; los runs se guardan en `runs/` y se verifican con `python scripts/verify_behavioral_run.py <run.json>`. Por defecto, el verificador exige que `skill_commit` coincida con el `HEAD` actualmente checkout; para una revisión histórica explícita puede pasarse `--expected-commit <sha>`. El verificador comprueba cobertura, commit y consistencia, pero no inventa los juicios semánticos.

## Baseline jurídico

Los casos que contienen afirmaciones regulatorias se apoyan en `references/sources-ar.md`. Si cambia ese baseline, se deben revalidar las afirmaciones legales embebidas en los evals antes de una release.