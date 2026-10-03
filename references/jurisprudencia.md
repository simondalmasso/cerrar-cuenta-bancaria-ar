# Jurisprudencia bancaria: cuándo y cómo usarla

## Regla principal

La jurisprudencia **no reemplaza** la norma BCRA que define el canal, requisitos o efectos operativos del cierre. Para una baja normal, resolver primero con [sources-ar.md](sources-ar.md), el sitio oficial del banco y el árbol operativo.

Activar jurisprudencia cuando exista una controversia real:
- pedido de baja que no fue efectivizado;
- cargos nuevos después de una baja o saldo cero;
- deuda residual no explicada;
- reporte BCRA/Veraz u otro perjuicio crediticio;
- incumplimiento de un acuerdo de consumo;
- deber de información o trato digno;
- daño económico por demoras o prácticas reiteradas.

Los antecedentes verificados están estructurados en [../registry/case-law.json](../registry/case-law.json).

## Dossier verificado

| Caso | Qué aporta a la skill | Uso |
|---|---|---|
| **CSJN, PADEC c/ BankBoston, Fallos 340:172 (14/03/2017)** | Tutela reforzada del consumidor en contratos bancarios y control de prácticas/cargos aun cuando exista regulación bancaria. | Encuadre general; cargos o cláusulas discutidas. |
| **Schvind c/ Compañía Financiera Argentina, CABA Sala II (14/03/2024)** | Cargos posteriores a baja/saldo cero no explicados, falta de información y reporte negativo al BCRA. | Caso directo para deuda/cargo residual posterior al cierre. |
| **Francoz c/ Banco Itaú, La Plata Sala I (13/03/2025)** | Baja no efectivizada, cargos de renovación, Veraz y carga dinámica de la prueba sobre registros que controla el banco. | Muy útil cuando el usuario reclamó por teléfono/sucursal y el banco dice no tener registro. |
| **Quiroga Crespo c/ Banco Itaú, Córdoba (02/10/2019)** | Cambio unilateral de condiciones, cargos inesperados, información, trato digno y prueba en poder del banco. | Apoyo ante paquetes bonificados/cargos no informados. |
| **Ciferri c/ Banco Santander Río, CABA Sala II (18/11/2025)** | Incumplimiento o cumplimiento tardío de acuerdo COPREC y análisis de daño punitivo. | Escalamiento cuando ya existe acuerdo de consumo incumplido. |

## Cómo convertir un fallo en una acción útil

No responder con doctrina extensa. Extraer solo:
1. hecho comparable;
2. regla o criterio judicial relevante;
3. diferencia material con el caso del usuario;
4. evidencia que conviene pedir o conservar;
5. etapa en la que el antecedente sirve: reclamo, COPREC/Defensa del Consumidor o litigio.

Ejemplos de impacto operativo:
- Si el banco afirma que nunca recibió una baja telefónica, **Francoz** refuerza la necesidad de pedir registros de llamadas/reclamos y no asumir que la ausencia de un formulario firmado resuelve la cuestión.
- Si la cuenta/producto quedó en cero y meses después aparecen cargos no explicados, **Schvind** justifica exigir composición, fecha de devengamiento, notificación y fundamento antes de tratar el pago como reconocimiento de deuda.
- Si existe acuerdo conciliatorio incumplido, **Ciferri** vuelve relevante documentar vencimiento, pago tardío y ejecución del acuerdo.

## Daño punitivo

Los antecedentes que tratan daño punitivo **no** crean una indemnización automática ni una suma estándar. Es una cuestión judicial dependiente de hechos, prueba y jurisdicción. En reclamos administrativos, usar el antecedente solo para contextualizar la gravedad alegada o preservar evidencia; no prometer condena, no trasladar montos de otro expediente y no presentar una cifra como derecho adquirido.

## Jerarquía de búsqueda

1. Corte Suprema / Secretaría de Jurisprudencia.
2. Tribunal oficial que dictó el fallo: JUBA-SCBA, JURISTECA-CABA, Justicia Córdoba u otro Poder Judicial.
3. SAIJ para discovery o texto cuando esté disponible.
4. MCP jurídicos read-only para localizar material.
5. Buscadores generales, Exa, Parallel, Tavily, Liner u otros: **solo discovery**.
6. Doctrina/comentarios privados: solo orientación; nunca como cita final si existe fuente oficial.

## Ficha mínima

Para incorporar un nuevo antecedente exigir: tribunal/sala, jurisdicción, fecha, carátula, expediente/fallo, hecho comparable, criterio relevante, diferencia material, URL oficial y estado `VERIFIED_OFFICIAL`, `REFERENCE` o `UNVERIFIED`.

## Regla de lenguaje

No decir “este fallo obliga al banco” ni extrapolar automáticamente una condena. Preferir:

> “Este antecedente muestra cómo un tribunal trató un problema comparable. Sirve como apoyo para el reclamo, pero la regla operativa de cierre sigue dependiendo de la normativa BCRA vigente, el producto y los hechos probados.”

## Investigación y actualización

La búsqueda puede usar múltiples motores para no depender de un único índice, pero el dato incorporado al dossier debe volver a una publicación judicial oficial. Ver [../docs/RESEARCH-STACK.md](../docs/RESEARCH-STACK.md).
