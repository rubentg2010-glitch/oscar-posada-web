# Mecánico a domicilio – Oscar Posada
Web estática en `public/` + Netlify Functions para las opiniones de clientes.

- Publicación: Netlify, carpeta `public`, funciones en `netlify/functions`.
- Opiniones: se guardan en Netlify Blobs. Los visitantes las envían, quedan pendientes y se aprueban en `/admin.html`.
- Variable de entorno necesaria en Netlify: `ADMIN_PASSWORD` (contraseña de la página de administración).

## Páginas por zona
`tools/gen_zonas.py` genera una página por municipio (`public/mecanico-a-domicilio-<zona>/`) y el `sitemap.xml`.
Para añadir o quitar zonas, edita la lista `Z` del script y ejecuta `python3 tools/gen_zonas.py`.
