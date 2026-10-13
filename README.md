# Altamirano Nosiglia — Landing page

Sitio estático de un solo archivo (`index.html`), listo para GitHub Pages.

## Configuración

Todos los datos se editan en el bloque `<script>` al final de `index.html`:

- `EMPRESA`: número de WhatsApp (formato internacional, solo dígitos), teléfono, email, redes, dirección, horarios y logo. Los campos vacíos no se muestran.
- `IMAGENES`: URLs de las fotos reales de cada sección. Mientras estén vacías se muestran ilustraciones de referencia.
- `DESTINOS`: tarjetas de destinos (de referencia, editables).
- `PROXIMOS_VIAJES`: salidas confirmadas. Si está vacío, se muestra un mensaje que invita a consultar.
- `OPCIONES_DESTINO` / `TIPOS_VIAJE`: opciones del formulario turístico.
- `MENSAJES`: textos predeterminados de WhatsApp.

Hasta que se cargue `EMPRESA.whatsapp`, los botones de WhatsApp muestran un aviso de configuración pendiente en lugar de abrir un enlace inválido.

## GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → Branch: `main` / `(root)`.
