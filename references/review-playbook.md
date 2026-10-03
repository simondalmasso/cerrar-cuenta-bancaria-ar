# Review playbook del expediente

Este playbook agrega una capa de **consistencia de revisión** sin cambiar la lógica jurídica ni el árbol A–G.

Su antecedente conceptual es el patrón de “rulebooks” usado por herramientas de revisión jurídica como Prism Legal OS: criterios reutilizables, explicables y separados del resultado final. En este repo se implementa de forma independiente y mínima, sin copiar código ni texto de Prism y sin convertirlo en dependencia.

Archivo machine-readable: [../registry/review-playbook.json](../registry/review-playbook.json).

## Cuándo usarlo

- **FAST:** normalmente no mostrar el playbook.
- **LIVE:** no usarlo en pantalla salvo que detecte un blocker inmediato.
- **FORENSIC:** usarlo como stage gate antes de escalar, cerrar el expediente o preparar un handoff importante.

También puede ejecutarse manualmente cuando una auditoría necesita comprobar que el caso no tiene huecos obvios.

## Estados

Cada check solo puede quedar en:

- `SATISFIED`
- `OPEN`
- `NOT_APPLICABLE`

No producir porcentajes, scores jurídicos ni “nivel de cumplimiento”. El objetivo es detectar gaps, no certificar legalidad.

## Reglas

1. Un check satisfecho necesita la evidencia indicada cuando `evidence_required=true`.
2. `OPEN` debe convertirse en un `OPEN_GAP` si puede cambiar la próxima acción.
3. `NOT_APPLICABLE` requiere una razón breve.
4. No convertir un resultado del playbook en una conclusión jurídica independiente.
5. Si un check depende de una norma o plazo, verificar la fuente oficial vigente.
6. El humano decide si avanzar; el playbook no presenta reclamos ni opera el banco.

## Salida recomendada

En modo FORENSIC:

| Check | Estado | Evidencia | Gap / próxima acción |
|---|---|---|---|
| PE-01 | SATISFIED | reclamo #... | — |
| PE-04 | OPEN | — | verificar fuente oficial vigente |

Solo mostrar checks relevantes para la etapa actual.

## Qué aporta y qué no

Aporta:
- revisión repetible entre agentes;
- menos omisiones antes de escalar;
- handoffs más claros;
- trazabilidad de por qué un caso se considera listo para avanzar.

No aporta:
- asesoramiento legal;
- certificación de cumplimiento;
- autoridad normativa;
- automatización del banco.
