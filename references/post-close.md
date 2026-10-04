# Protocolo post-cierre

La constancia de cierre no termina por sí sola el expediente. Separar **cierre informado**, **cierre verificado** y **monitoreo post-cierre**.

## T0 — al recibir la constancia

Confirmar:
- banco y producto exacto;
- identificador parcial correcto;
- fecha efectiva;
- saldo final **por producto y moneda**;
- si el paquete incluía otros contratos;
- qué productos siguen abiertos;
- último resumen/movimiento disponible;
- número de gestión o constancia.

Si falta alguno de esos elementos materiales, mantener **F — Cierre informado**.

## Paso a G — cierre verificado

Puede pasar a **G** cuando existe evidencia suficiente de que el producto correcto fue cerrado y no hay cuestiones abiertas atribuibles al mantenimiento de esa cuenta.

`G` no significa “nunca puede aparecer otra controversia”. Significa que, con la evidencia disponible, el cierre está verificado.

## Alcance de G

`G — Cierre verificado` se refiere **al producto objetivo identificado**, no a la extinción automática de todo vínculo con el banco. En handoffs machine-readable, identificar ese producto con un `target_product_ref` local del caso (`P-001`, `P-002`, etc.), nunca con el número completo de cuenta/tarjeta. Una tarjeta, préstamo, seguro u otro contrato vinculado puede seguir abierto si quedó expresamente separado y documentado.

Antes de G, verificar que los vinculados relevantes fueron: **cerrados**, **confirmados como aún abiertos por decisión/contrato independiente**, o **separados como tema residual**. Para cada saldo residual, registrar al menos **producto, moneda, importe y disposición prevista**. En `related_products[]`, no dejar `status=unknown` al pasar a G. No exigir cerrar un producto distinto solo por estar vinculado.

## Monitoreo posterior

Registrar `post_close_status`:

- `not_started`: constancia recibida, todavía sin control posterior;
- `monitoring`: esperando próximo ciclo/resumen o actualización relevante;
- `clear`: control posterior sin anomalías materiales;
- `issue_found`: apareció un cargo, reapertura, reporte o inconsistencia.

Revisar cuando sea razonablemente aplicable:
1. próximo resumen o ciclo de movimientos;
2. cargos/comisiones posteriores;
3. débitos o liquidaciones pendientes previamente identificadas;
4. productos vinculados que sigan vigentes;
5. registros crediticios si existía deuda/reporting o un antecedente concreto que lo justifique.

No convertir una demora normal de actualización de un registro externo en prueba automática de reapertura o incumplimiento. Registrar fecha, fuente y diferencia.

## Si aparece un cargo posterior

Volver a separar:
- fecha de devengamiento;
- fecha de contabilización/débito;
- capital/interés/impuesto/comisión;
- relación con períodos anteriores al cierre;
- notificación y fundamento.

Un importe puede ser matemáticamente correcto y jurídicamente discutible.

Si el nuevo hecho reabre una controversia, conservar G como hito histórico del cierre verificado y marcar `post_close_status=issue_found`; abrir un evento nuevo en el timeline en lugar de borrar la historia anterior.