# Adversarial eval specifications

`scenarios.json` contiene **especificaciones** de comportamiento esperado. No son, por sí solas, ejecuciones de un modelo.

`scripts/validate_repo.py` valida estructura:
- ID y nombre únicos;
- `prompt` no vacío;
- `must` no vacío;
- `must_not` no vacío;
- strings válidos.

El CI distingue explícitamente:
- **structure pass**;
- **behavioral agent eval execution: NOT RUN**.

## Runner por host

Cada proveedor/host puede convertir el mismo caso en una prueba conductual:

1. cargar la skill;
2. enviar `prompt`;
3. capturar respuesta y tool calls;
4. evaluar cada condición `must`;
5. evaluar cada prohibición `must_not`;
6. conservar modelo, versión, fecha y herramientas disponibles.

Un runner conductual no debe recibir credenciales bancarias reales ni operar servicios externos. Para casos de tool-use, usar mocks/sandboxes read-only.
