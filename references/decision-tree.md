# Árbol de decisión operativo

## Paso 0 — ¿Es una cuenta bancaria argentina?

Confirmar banco y producto. Si es una billetera/PSP, tarjeta aislada, broker o fintech no bancaria, no aplicar automáticamente estas reglas.

## Paso 0.5 — ¿Hay una condición especial?

Si aparece cotitularidad, apoderado, fallecimiento, menor, embargo/inhibición, bloqueo judicial o residencia en el exterior, leer [special-cases.md](special-cases.md). Mantener el estado A–G y agregar el flag correspondiente; no forzar el árbol estándar hasta resolver el `OPEN_GAP` especial.

## Paso 1 — Tipo de producto

### Caja de ahorro / depósito a la vista
Ruta normal: cierre remoto + constancia.

### Cuenta corriente
Preguntar dos cosas antes de afirmar el canal:
1. ¿prevé uso de cheques/ECHEQ?
2. ¿registra saldo deudor?

- Sin cheques + sin saldo deudor: rama remota fuerte.
- Con saldo deudor: la norma específica asegura al menos cierre presencial en cualquier sucursal. Intentar resolver remotamente puede ser posible, pero no venderlo como derecho garantizado.
- Con cheques/ECHEQ: revisar obligaciones sobre cheques pendientes y devolución/anulación.

### Cuenta sueldo / seguridad social / especial
No usar la regla general como única respuesta. Verificar el régimen específico vigente y si existen acreditaciones periódicas que afectan el cierre.

### Paquete multiproducto
Descomponer:
- cuenta/s;
- tarjeta/s;
- préstamo/s;
- inversión/es;
- seguro/s;
- caja de seguridad;
- beneficios.

El cierre del paquete no prueba el cierre de cada contrato y viceversa.

## Paso 2 — Estado del saldo

Registrar primero la **moneda**. Si existen saldos en más de una moneda o componentes compensados, separar cada componente y su neto; no convertir un neto global en “cero” sin analizar la exposición de cada cuenta/moneda.

### Positivo
Objetivo: determinar qué requiere el canal para disponer del saldo. No mover dinero por el usuario.

Preguntas útiles:
- "¿El cierre puede completarse transfiriendo el remanente?"
- "¿Qué pasa con los fondos si solicito el cierre hoy?"
- "¿Me entregan constancia en el mismo acto?"

### Cero
No seguir buscando "saldo oculto" sin señal concreta. Pasar a bloqueos operativos.

### Negativo / descubierto
Separar:
- capital;
- interés;
- tasa;
- período;
- impuestos;
- cargos/comisiones;
- fecha de contabilización.

Preguntar:
- "¿Cuál es el importe total exacto para regularizar hoy?"
- "¿Incluye intereses e impuestos ya devengados?"
- "¿Puede quedar algún residual a liquidar después?"
- "¿Con este pago queda el saldo deudor en cero?"
- "¿La solicitud vigente sigue activa?"

No asumir que pagar un saldo elimina automáticamente la necesidad de reingresar el cierre.

### Incierto
Pedir al usuario captura o texto de la pantalla de saldo/movimientos, con datos sensibles redactados.

## Paso 3 — ¿Ya existe solicitud?

### No
Preparar:
- ruta oficial del banco;
- requisitos mínimos;
- qué capturar;
- texto alternativo para chat/telefonía.

### Sí, pendiente
No duplicar solicitudes por ansiedad salvo que el banco confirme que la anterior quedó cerrada/rechazada. Duplicar puede fragmentar evidencia.

### Sí, rechazada con causa
Tratar la causa; luego preguntar si:
- la gestión original revive;
- debe crearse una nueva;
- existe período de espera.

### Sí, rechazada sin causa
Pedir por escrito:
- motivo exacto;
- producto que bloquea;
- importe si hay deuda;
- norma/condición contractual invocada;
- número de reclamo.

## Paso 4 — Productos vinculados

Solo investigar si hay señal.

### Tarjeta
No asumir que el saldo de tarjeta impide cerrar la cuenta. Verificar contrato y la instrucción concreta del banco. Mantener separado:
- baja de cuenta;
- baja de tarjeta;
- deuda/saldo a favor de tarjeta.

### Préstamo
Determinar medio alternativo de pago antes de cerrar la cuenta si el préstamo debita allí.

### Débitos automáticos
Listar los próximos débitos relevantes. El usuario decide su migración/baja.

### Inversiones
No vender ni rescatar. Identificar si dependen operativamente de la cuenta y explicar la pregunta a hacer al banco.

### Caja de seguridad
No inferir bloqueo. Solo activar esta rama si:
- el banco la menciona;
- el contrato la liga al paquete/cuenta;
- hay un débito de alquiler pendiente que impacta la cuenta.

Preguntar: "¿La caja de seguridad impide técnicamente el cierre de esta cuenta? Si sí, ¿qué contrato o condición lo establece?"

## Paso 5 — Presencialidad

Si el banco exige sucursal:
1. clasificar tipo de cuenta;
2. verificar saldo deudor;
3. verificar cheques;
4. buscar regla actual BCRA;
5. si la rama remota aplica, pedir fundamento escrito y abrir reclamo;
6. si la norma específica solo garantiza presencialidad, no inventar una obligación remota.

Objetivo: evitar presencialidad innecesaria, no negarla cuando la norma específica la contempla.

## Paso 6 — Loop

Definir loop como dos o más ciclos en los que:
- se corrige el motivo informado;
- se vuelve a solicitar;
- el banco rechaza o deriva nuevamente sin identificar una causa nueva verificable.

En loop:
- dejar de repetir la misma operación;
- construir timeline;
- abrir reclamo formal;
- pedir causa única y exhaustiva;
- solicitar que identifiquen todos los blockers restantes en una sola respuesta.

Frase:
"Ya regularicé el impedimento informado en la gestión anterior. Necesito que identifiquen de forma completa cualquier impedimento restante para el cierre y me den un número de reclamo."

## Paso 7 — Cierre

Verificar:
- constancia;
- fecha efectiva;
- producto exacto;
- saldo final;
- cargos posteriores;
- temas vinculados residuales.

Solo entonces pasar a G. Después aplicar [post-close.md](post-close.md): registrar `post_close_status`, revisar anomalías razonables y no confundir una incidencia posterior con que el hito histórico de cierre nunca existió.
