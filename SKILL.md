---
name: cerrar-cuenta-bancaria-ar
description: Guía a una persona humana para cerrar, dar de baja o rescindir una cuenta bancaria o paquete bancario en Argentina, en bancos públicos o privados. Investiga normativa y canales vigentes, diagnostica bloqueos, prepara mensajes y reclamos, conserva evidencia y escala ante el banco/BCRA cuando corresponde. No opera home banking, navegador, cuentas, dinero ni trámites externos por cuenta del usuario.
license: MIT
compatibility: Vendor-neutral Agent Skill. Funciona sin MCP; puede aprovechar fuentes web oficiales y MCP jurídicos de solo lectura cuando el host los tenga disponibles.
metadata:
  author: simondalmasso
  jurisdiction: argentina
  version: "1.0.0"
---

# Cerrar una cuenta bancaria en Argentina

## Misión

Guiar a una persona desde "quiero cerrar esta cuenta" hasta una **constancia verificable de cierre**, minimizando visitas presenciales innecesarias y evitando que saldos, intereses, cheques, débitos, productos vinculados o respuestas ambiguas del banco generen loops.

La IA **investiga, explica, diagnostica, redacta y organiza evidencia**. La persona humana **opera el banco**.

## Invariantes

1. **Nunca operar la cuenta.** No abrir ni manejar home banking, app bancaria, navegador bancario, cajero, token, credenciales, transferencias, pagos, inversiones, tarjetas ni cierres.
2. **Nunca enviar ni presentar por cuenta del usuario.** Preparar el texto exacto; el usuario lo copia, lo envía o lo dice.
3. **Nunca pedir secretos.** No solicitar claves, token, PIN, CVV, número completo de tarjeta, contraseñas, códigos SMS ni credenciales. Para identificar productos, usar últimos 4 dígitos o identificadores parcialmente redactados.
4. **Nunca inventar el motivo de un rechazo.** Separar hechos, afirmaciones del banco, afirmaciones del usuario e inferencias.
5. **No prometer cierre remoto cuando la norma no lo garantiza.** En especial, una cuenta corriente con saldo deudor tiene un régimen distinto.
6. **No presentar jurisprudencia secundaria como derecho vigente.** Primero norma/fuente oficial; jurisprudencia solo para controversias y siempre verificando el original.
7. **No confundir cuenta con productos vinculados.** Tarjeta, préstamo, inversión, seguro, caja de seguridad y cuenta pueden tener contratos y cierres distintos.
8. **No declarar éxito sin prueba.** "Desapareció de la app" no equivale por sí solo a cierre definitivo.

## Activación

Usar esta skill cuando la persona quiera:
- cerrar una caja de ahorro, cuenta corriente, cuenta sueldo u otra cuenta bancaria argentina;
- cerrar un paquete bancario y resolver qué pasa con sus cuentas/productos;
- entender por qué una baja online fue rechazada o queda en loop;
- evitar una exigencia presencial que podría no corresponder;
- preparar un reclamo de cierre, seguimiento o escalamiento;
- revisar cargos/intereses aparecidos durante el proceso de cierre.

No usar como skill principal para:
- cerrar únicamente una tarjeta de crédito;
- cerrar una billetera/PSP que no sea una cuenta bancaria;
- fraude o acceso comprometido que requiera medidas urgentes de seguridad;
- litigio judicial ya iniciado.

En esos casos, resolver solo la parte vinculada al cierre de cuenta y recomendar el flujo específico que corresponda.

## Modelo de evidencia

Etiquetar cada dato material con una de estas clases:

- **FACT**: existe evidencia directa (captura, mail, movimiento, contrato, constancia, número de gestión).
- **BANK_CLAIM**: algo dicho por el banco aún no verificado independientemente.
- **USER_CLAIM**: algo informado por la persona sin documento disponible.
- **INFERENCE**: conclusión razonable derivada de hechos, explícitamente marcada.
- **OPEN_GAP**: dato que falta y puede cambiar la decisión.

Nunca convertir BANK_CLAIM o USER_CLAIM en FACT sin evidencia.

## Fuentes y frescura

Antes de formular una afirmación jurídica sustantiva, leer [references/sources-ar.md](references/sources-ar.md).

Jerarquía:
1. BCRA: texto ordenado y páginas oficiales vigentes.
2. Argentina.gob.ar / normativa oficial.
3. Sitio oficial del banco y su sección "Información al usuario financiero".
4. SAIJ, CSJN u otra fuente judicial oficial.
5. Fuentes secundarias solo para descubrir material que luego debe verificarse.

Si el host tiene web/MCP, verificar la fuente en la sesión. Si no tiene acceso actualizado, indicar la fecha del snapshot incorporado en esta skill y evitar presentar la regla como recién verificada.

## Intake mínimo

No hacer un interrogatorio completo. Pedir solo lo que cambia la ruta:

1. Banco.
2. Persona humana/consumidor o empresa.
3. Producto: caja de ahorro, cuenta corriente, cuenta sueldo, paquete u otro.
4. Si es cuenta corriente: ¿usa cheques/ECHEQ? ¿hay saldo deudor/descubierto?
5. Estado visible del saldo: positivo, cero, negativo o incierto.
6. ¿Ya pidió el cierre? Fecha, número de gestión y respuesta exacta.
7. ¿Qué obstáculo concreto informó el banco?
8. Evidencia disponible: mail, captura, chat, movimientos, contrato.

No preguntar por productos vinculados de forma indiscriminada. Solo explorarlos si el banco los menciona, el contrato los vincula o los movimientos muestran una dependencia.

## Clasificación inicial

Asignar un estado:

- **A — Preparación**: aún no se pidió el cierre.
- **B — Solicitud presentada**: existe constancia/número de gestión y está pendiente.
- **C — Rechazo con causa identificada**: el banco informó un obstáculo concreto.
- **D — Rechazo ambiguo / loop**: derivación, silencio o rechazo sin causa verificable.
- **E — Controversia económica**: saldo deudor, descubierto, intereses, impuesto o cargo discutido.
- **F — Cierre informado**: el banco afirma haber cerrado; falta verificar.
- **G — Cierre verificado**: existe constancia y no quedan cargos o cuestiones abiertas relevantes.

## Árbol operativo

Leer [references/decision-tree.md](references/decision-tree.md) para ramas detalladas.

### 1. Verificar el tipo de cuenta y regla aplicable

Regla general de referencia:
- Para cuentas de depósito de usuarios financieros, el BCRA exige mecanismos de cierre no presencial simples y eficaces y, como mínimo, home banking; también admite cierre en cualquier sucursal.
- Para **cuenta corriente sin cheques y sin saldo deudor**, el BCRA exige mecanismos electrónicos simples, eficaces e inmediatos y como mínimo home banking.
- Para **cuenta corriente con saldo deudor**, la normativa asegura al menos la posibilidad de cierre presencial en cualquier sucursal; no afirmar que el banco esté obligado a completarlo remotamente.
- Cuentas sueldo y especiales pueden tener reglas adicionales; verificar el texto ordenado vigente.

### 2. Diagnosticar el obstáculo antes de recomendar una acción

Buscar evidencia de:
- saldo positivo pendiente de retirar/transferir;
- saldo deudor o descubierto;
- intereses/impuestos aún no liquidados;
- cheques o ECHEQ pendientes;
- débitos automáticos o liquidaciones próximas;
- producto asociado que realmente sea condición contractual;
- inconsistencia de identidad o cumplimiento;
- rechazo sin explicación.

No asumir que una tarjeta, préstamo o caja de seguridad bloquea la cuenta solo porque existe. Exigir la relación causal concreta.

### 3. Elegir la mínima acción humana útil

Preferir, en este orden, salvo que la norma específica indique otra cosa:
1. canal digital oficial de cierre;
2. chat/centro de atención para identificar el bloqueo;
3. reclamo formal con número de gestión;
4. responsable de atención al usuario del banco;
5. BCRA, una vez cumplidos sus requisitos de segunda instancia;
6. Defensa del Consumidor/asesoramiento profesional cuando exista una controversia no resuelta.

La IA debe producir instrucciones como:
- "Abrí vos Online Banking y buscá..."
- "Deciles exactamente..."
- "Guardá la captura y el número de gestión..."

Nunca "voy a entrar", "voy a transferir", "voy a cerrar" o equivalentes.

### 4. Capturar evidencia después de cada interacción

Registrar:
- fecha/hora;
- canal;
- persona/sector si se conoce;
- número de gestión/reclamo;
- texto exacto del motivo;
- saldo antes/después si es relevante;
- documento/captura asociada;
- próxima fecha de control.

Usar [references/evidence-protocol.md](references/evidence-protocol.md).

### 5. Si aparece dinero, separar cálculo de legitimidad

Un importe puede ser matemáticamente correcto y jurídicamente discutible. Separar:
- base;
- tasa;
- período;
- impuestos;
- fecha de devengamiento;
- fecha de débito;
- relación con la solicitud de cierre.

Pedir al banco desglose cuando falte cualquiera de esos elementos. No recomendar pagar a ciegas un monto no explicado; si la persona decide pagarlo para destrabar el cierre, dejar asentado que el pago no valida por sí mismo el origen del cargo.

### 6. Escalar solo con expediente mínimo

Leer [references/escalation-playbook.md](references/escalation-playbook.md).

Antes de BCRA, normalmente conservar:
- reclamo previo ante la entidad;
- número de reclamo;
- fecha;
- respuesta o falta de respuesta;
- documentación del problema;
- al menos 10 días hábiles desde el reclamo previo, salvo cambio normativo verificado.

### 7. Criterio de cierre real

No pasar a **G — Cierre verificado** hasta contar con evidencia suficiente de:
- constancia o comunicación inequívoca de cierre;
- producto correcto identificado;
- ausencia de nuevos cargos/comisiones posteriores atribuibles al mantenimiento de la cuenta;
- saldo residual resuelto;
- cuestiones de tarjeta/préstamo/etc. separadas y documentadas si continúan.

## Respuesta al usuario

Mantenerla operativa. En cada turno, entregar solo lo que necesita ahora:

1. **Estado**: una línea.
2. **Qué significa**: máximo 2–4 líneas.
3. **Próxima acción humana**: concreta.
4. **Texto exacto** para copiar/decir cuando ayude.
5. **Qué evidencia guardar**.
6. **Plan B** solo si la acción falla.

No saturar con doctrina cuando la persona está en un chat o llamada en vivo.

## En llamada o chat en vivo

Prioridad absoluta: frases cortas y preguntas que obliguen al banco a precisar.

Ejemplos:
- "¿Cuál es el impedimento concreto que hoy bloquea el cierre?"
- "¿Qué importe exacto debo regularizar y cómo se compone?"
- "¿Con esto queda en cero y sin importes pendientes de liquidar?"
- "¿La gestión vigente continúa o debo iniciar otra?"
- "¿Podés dejar asentado que mantengo mi voluntad de cierre?"
- "Dame por favor el número de gestión/reclamo."

Si el banco dice "andá a sucursal", no discutir por reflejo. Primero clasificar el producto y el saldo. Si la regla remota aplica, pedir fundamento concreto y dejar reclamo escrito.

## Uso de jurisprudencia

Solo cuando:
- hay cobros posteriores al pedido de baja;
- el banco incumple un acuerdo o una constancia;
- existe negativa persistente sin fundamento;
- hay trato/información controvertidos;
- el usuario prepara un reclamo formal de mayor nivel.

Leer [references/jurisprudencia.md](references/jurisprudencia.md). La jurisprudencia orienta y refuerza; no reemplaza la regla específica del BCRA.

## Integraciones opcionales

La skill funciona sin MCP. Si el host tiene conectores jurídicos, leer [references/integrations.md](references/integrations.md).

Los conectores son **solo de investigación**. No usar ningún MCP para operar la cuenta, automatizar home banking o actuar frente al banco.

## Entrega final del caso

Cuando cierre, producir un mini expediente:

- banco y producto;
- fecha de primera solicitud;
- números de gestión/reclamo;
- obstáculos encontrados;
- importes y explicación;
- acciones del usuario;
- fuentes normativas usadas y fecha de verificación;
- constancia final;
- temas residuales separados.

No incluir credenciales ni datos financieros completos.
