# Protocolo de evidencia

## Objetivo

Convertir chats, llamadas, mails, capturas y movimientos en un expediente breve que permita:
- saber qué pasó;
- evitar repetir gestiones;
- demostrar qué informó el banco;
- separar hechos de hipótesis;
- escalar con un relato consistente.

## Registro mínimo por evento

| Campo | Contenido |
|---|---|
| ID | E-001, E-002... |
| Fecha/hora | exacta si se conoce |
| Canal | home banking, app, chat, teléfono, mail, sucursal |
| Actor | usuario / banco / asesor identificado |
| Tipo | FACT / BANK_CLAIM / USER_CLAIM / INFERENCE / OPEN_GAP |
| Hecho | una oración |
| Gestión | número si existe |
| Importe | solo si relevante |
| Evidencia | archivo/captura/mail |
| Próximo paso | acción humana |
| Estado | abierto/cerrado |

## Reglas de calidad

- Una fila = un hecho material.
- No mezclar "el banco dijo" con "la norma exige".
- No interpretar una captura sin describir primero lo visible.
- Si un saldo muestra componentes compensados, registrar cada componente y el neto.
- Si una llamada no quedó grabada, usar BANK_CLAIM salvo que exista confirmación escrita posterior.
- Conservar los números de gestión aunque hayan sido rechazados.

## Minimización y ocultamiento seguro

Nunca incluir en el expediente, salvo necesidad estricta y aun así de forma parcialmente ocultada:
- DNI completo: usar solo últimos dígitos cuando alcance;
- CBU/CVU completo;
- número completo de cuenta;
- datos completos de tarjetas;
- domicilios innecesarios;
- teléfonos personales si el expediente se comparte.

Ocultar/tapar esos datos en capturas o documentos antes de compartirlos. Conservar solo el identificador parcial mínimo que permita distinguir el producto o la evidencia.

Nunca almacenar claves, token, PIN, CVV o códigos de verificación.

## Timeline recomendado

Columnas:
1. fecha/hora;
2. evento;
3. evidencia;
4. efecto sobre el cierre;
5. pendiente.

## Mapa de claims

Para cada afirmación importante:

| Claim | Evidencia | Fuente normativa | Confianza | Gap |
|---|---|---|---|---|
| "El saldo deudor bloqueó la baja" | chat asesor + saldo | régimen cuenta corriente | alta | confirmar si era causa única |
| "No corresponde comisión posterior" | fecha solicitud | BCRA actual | alta | distinguir interés/impuesto de comisión |
| "Producto X bloquea" | solo inferencia | ninguna | baja | pedir confirmación banco |

## Cierre probatorio

El expediente final debe poder responder:
- ¿cuándo se solicitó por primera vez?
- ¿qué impidió el cierre cada vez?
- ¿qué corrigió el usuario?
- ¿qué importes aparecieron y por qué?
- ¿qué números de gestión existen?
- ¿cuándo quedó cerrado?
- ¿qué prueba lo demuestra?
