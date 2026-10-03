# Casos especiales — desvíos controlados

Estas ramas existen para **detener la extrapolación automática** del flujo estándar. No cambian el core: abren un desvío, identifican qué falta verificar y devuelven el control al humano.

## Regla común

Ante cualquiera de estas señales:
1. mantener el estado A–G del expediente;
2. agregar el `special_case_flag` correspondiente;
3. no inventar representación, capacidad, facultades ni levantamiento de medidas;
4. verificar fuente oficial/banco/expediente aplicable;
5. si hay proceso judicial o sucesorio, separar la parte bancaria de la cuestión jurídica principal.

## Cotitulares

No asumir que un cotitular puede cerrar unilateralmente toda la relación.

Verificar:
- modalidad de firma/operación;
- contrato del producto;
- si el pedido afecta solo la participación de una persona o la cuenta completa;
- qué consentimiento exige el banco.

Pregunta operativa: “¿El cierre completo requiere intervención de los demás cotitulares? Indiquen la regla contractual o normativa aplicable.”

## Apoderados

No asumir que cualquier poder habilita a cerrar cuentas.

Verificar:
- vigencia del poder;
- facultades expresas;
- forma de acreditación aceptada por el banco;
- si existe restricción para actos de disposición o cierre.

La IA no valida autenticidad notarial ni suplanta al banco/notario.

## Fallecimiento del titular

Salir del flujo normal de baja voluntaria.

Prioridad:
- identificar si existe cotitular;
- pedir al banco el procedimiento oficial para fallecimiento/sucesión;
- no instruir movimientos de fondos;
- no asumir quién tiene legitimación hereditaria.

## Menores

Verificar representación y régimen del producto antes de aplicar la ruta ordinaria.

No asumir que:
- el menor puede cerrar solo;
- un progenitor/tutor puede hacerlo sin acreditación;
- las reglas del producto adulto aplican sin matices.

## Embargo / inhibición / medida judicial

No sugerir maniobras para eludir o vaciar una medida.

Pedir:
- qué medida concreta invoca el banco;
- juzgado/expediente/oficio si está disponible;
- qué aspecto impide: disponibilidad, transferencia, cierre o solo fondos.

Si la controversia depende de una orden judicial, marcar `OPEN_GAP` y derivar el aspecto jurídico correspondiente.

## Cuenta judicialmente bloqueada

Distinguir:
- bloqueo interno/compliance;
- orden judicial;
- medida cautelar;
- restricción operativa no explicada.

Una cuenta con intervención judicial no debe tratarse como simple “rechazo de baja”.

## Residencia en el exterior

No prometer presencialidad local ni cierre remoto universal.

Verificar:
- canal remoto oficial;
- representación/apoderado si fuera necesario;
- requisitos de identidad;
- posibilidad de gestionar desde consulado u otro canal solo si una fuente oficial lo confirma.

## Salida

Estas ramas no crean estados H/I/J. El estado A–G sigue describiendo **dónde está el cierre**; `special_case_flags` describe **por qué el árbol estándar necesita una verificación adicional**.
