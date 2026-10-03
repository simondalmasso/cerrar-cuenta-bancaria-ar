# Perfiles bancarios opcionales

El core no tiene un banco protagonista y no debe hardcodear menús, URLs o políticas de una entidad dentro de `SKILL.md`.

Si en el futuro se agregan perfiles específicos, usar archivos bajo:

`banks/<id>/discovery.json`

Cada perfil debe:
- derivarse de web oficial pública;
- incluir `checked_at`;
- distinguir norma BCRA de política/canal del banco;
- contener solo rutas públicas, nunca credenciales ni sesiones;
- degradar a discovery en vivo si queda desactualizado;
- no modificar la lógica jurídica core.

No crear un perfil a partir de capturas, chats o cuentas reales de usuarios.
