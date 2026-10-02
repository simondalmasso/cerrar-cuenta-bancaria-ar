# Investigación del banco específico

## Objetivo

Encontrar el procedimiento **actual y oficial** del banco sin hardcodear instrucciones que puedan quedar viejas. Esta skill debe funcionar con cualquier banco público o privado regulado en Argentina.

## 1. Confirmar identidad regulatoria

Primero verificar la entidad en:
- https://www.bcra.gob.ar/entidades-financieras

Registrar:
- denominación legal;
- nombre comercial;
- código de entidad si está disponible;
- condición de entidad financiera;
- fecha de consulta.

Si la entidad no aparece, no aplicar automáticamente el régimen bancario. Puede tratarse de un PSP, cooperativa, fintech u otra figura.

## 2. Encontrar únicamente fuentes oficiales del banco

Buscar en el dominio oficial:
- "cerrar cuenta";
- "baja de cuenta";
- "baja de paquete";
- "información al usuario financiero";
- "reclamos";
- "responsable de atención al usuario";
- contrato/condiciones del producto;
- cuadro de comisiones.

No usar blogs SEO, foros ni agregadores como fuente de procedimiento.

## 3. Registrar una ficha de banco

Usar assets/templates/bank-profile.md.

Campos obligatorios:
- banco;
- URL oficial;
- página de cierre;
- canales ofrecidos;
- condiciones/bloqueadores declarados;
- responsable de atención;
- fecha de verificación;
- fuente de cada dato.

## 4. Separar política interna de obligación normativa

Etiquetas:
- **LAW/RULE**: BCRA/ley aplicable.
- **BANK_POLICY**: instrucción del banco.
- **BANK_CLAIM**: algo dicho por un asesor.
- **INFERENCE**: conclusión del agente.

Si BANK_POLICY es más restrictiva que una regla BCRA aparentemente aplicable, no afirmar incumplimiento de inmediato. Confirmar producto, saldo, cheques y versión vigente; luego pedir fundamento por escrito.

## 5. Evitar rutas viejas

Una captura o guía histórica puede probar qué vio el usuario, pero no necesariamente el procedimiento actual.

Antes de decir "hacé clic en X":
1. confirmar que la página oficial actual sigue mostrando esa ruta;
2. si no se puede verificar, describir el objetivo ("buscá la opción de cierre/baja") sin inventar menús.

## 6. Cuando el banco no publica la causa del rechazo

No especular. Pedir:

> "Necesito que me indiquen el impedimento concreto y exhaustivo que bloquea el cierre de esta cuenta y el producto al que corresponde."

Guardar número de gestión/reclamo y respuesta exacta.

## 7. Banco público vs privado

La skill no cambia de criterio por propiedad estatal/privada. Primero determina:
- si es entidad financiera alcanzada;
- tipo de cuenta;
- condición de usuario;
- norma específica.

La titularidad pública del banco no elimina la obligación de verificar su régimen y procedimiento vigente.
