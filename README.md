# Altamirano Nosiglia — Landing page

Sitio estático de un solo archivo (`index.html`), listo para GitHub Pages.

## Configuración

Todos los datos se editan en el bloque `<script>` al final de `index.html`:

- `EMPRESA`: WhatsApp en formato internacional, solo dígitos (configurado: 5493794788375), dirección, enlace y mapa de Google Maps, teléfono, email, redes, horarios y logo. Los campos vacíos no se muestran.
- `IMAGENES`: fotos de cada sección. `foto("nombre")` usa `img/nombre-800.jpg` e `img/nombre-1600.jpg` (la portada llega a 3840 px). Si una foto falta o no carga, se muestra una ilustración de referencia.
- `CREDITOS`: autoría y licencia de cada foto (se muestran en el pie de página). Las fotos actuales son de Wikimedia Commons con licencias Creative Commons o dominio público; `img/creditos.json` guarda los datos de origen. Si se reemplaza una foto por una propia, hay que quitar su crédito.
- `DESTINOS`: tarjetas de destinos (de referencia, editables).
- `PROXIMOS_VIAJES`: salidas confirmadas. Si está vacío, se muestra un mensaje que invita a consultar.
- `OPCIONES_DESTINO` / `TIPOS_VIAJE`: opciones del formulario turístico.
- `MENSAJES`: textos predeterminados de WhatsApp.

Hasta que se cargue `EMPRESA.whatsapp`, los botones de WhatsApp muestran un aviso de configuración pendiente en lugar de abrir un enlace inválido.

## GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → Branch: `main` / `(root)`.
