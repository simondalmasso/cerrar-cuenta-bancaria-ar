# Saldos, intereses y bloqueadores

## Principio

Un "saldo total cero" no siempre describe todos los componentes contables, y un débito posterior a la solicitud no es automáticamente una comisión prohibida.

Separar siempre **matemática**, **naturaleza del concepto** y **legitimidad jurídica**.

Para cualquier saldo, descubierto o residual que involucre más de un producto/componente, registrar de forma explícita: **producto, moneda, importe y concepto**. Un total neto no reemplaza ese desglose.

## Matriz económica

### Saldo visible cero con residual contable

Un dashboard principal en `0` no demuestra por sí solo que no existan residuales. Si una vista detallada, subcuenta, resumen o liquidación muestra un importe negativo/positivo distinto de cero, o intereses todavía no contabilizados, no declarar el blocker resuelto.

Registrar por separado:
- producto;
- moneda;
- importe;
- concepto;
- período;
- tasa si corresponde;
- fecha de devengamiento;
- fecha de contabilización/débito;
- si el banco informa que habrá otra liquidación o residual.

Pregunta de cierre del blocker:

> "¿Queda algún interés, impuesto, ajuste o residual todavía por liquidar/contabilizar después de este movimiento?"

`saldo visible 0` puede ser FACT sobre esa vista; `no existen residuales` requiere evidencia adicional.


### Saldo positivo
- FACT: monto visible.
- Acción humana: disponer del saldo según la opción elegida por el usuario y el procedimiento aplicable.
- La IA no transfiere.
- Verificar si el banco permite cierre con fondos a saldos inmovilizados según la norma vigente.

### Saldo deudor / descubierto
Obtener:
- producto;
- moneda;
- capital/base;
- tasa aplicada;
- período de devengamiento;
- intereses;
- impuestos;
- fecha de liquidación;
- fecha de débito;
- monto final para quedar sin saldo deudor;
- posibilidad de residual posterior.

Para cuenta corriente, esta condición puede cambiar el canal mínimo de cierre exigible.

### Interés
Preguntar qué período remunera. Que se debite después de la solicitud no prueba que se haya devengado después.

### Comisión/cargo
Comparar fecha de solicitud de cierre y concepto exacto con la norma vigente. No llamar "comisión" a todo débito.

### Impuesto
Identificar base imponible, alícuota y concepto. Un impuesto puede derivar de un interés/débito anterior; analizar por separado.

## Productos asociados

### Tarjeta de crédito
Cuenta bancaria y tarjeta son contratos distintos salvo prueba específica. No afirmar que deuda o saldo a favor de tarjeta bloquea el cierre de cuenta sin:
- política/contrato aplicable; o
- confirmación concreta del banco.

La guía oficial argentina sobre tarjetas indica que la tarjeta puede darse de baja aun con deuda pendiente; la deuda continúa separadamente y puede seguir siendo reclamada por el emisor. Ver [sources-ar.md](sources-ar.md). Por eso, "esperá al vencimiento de la tarjeta" puede ser una conveniencia operativa o BANK_POLICY, no un blocker normativo automático del cierre de cuenta/paquete.

### Préstamo
Determinar cómo se pagará después del cierre. No instruir cancelación anticipada salvo que el usuario lo decida y comprenda el costo.

### Inversiones / plazo fijo
No vender ni rescatar. Identificar dependencia operativa y preguntar al banco por alternativa de custodia/transferencia/cobro.

### Débitos automáticos
Identificar próximos débitos relevantes; el usuario decide migración o baja.

### Caja de seguridad
No inferir bloqueo por mera titularidad/cotitularidad. Activar solo con evidencia contractual o BANK_CLAIM del banco.

### Cheques / ECHEQ
En cuenta corriente, tratarlos como rama especial. Verificar la reglamentación vigente antes de indicar cierre.

## Pregunta de exhaustividad

Después de resolver un blocker:

> "¿Con esto queda regularizado el impedimento y existe algún otro bloqueo pendiente que pueda impedir el cierre?"

## Pago para destrabar

Si el usuario decide pagar un importe:
- confirmar producto y moneda;
- confirmar monto total;
- preguntar si deja saldo deudor en cero;
- preguntar por residual;
- guardar comprobante;
- confirmar si la gestión anterior sigue viva.

El pago no convierte automáticamente en correcto el origen del cargo. Mantener separada cualquier impugnación.