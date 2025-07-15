# People Analytics: Aplicación Web de Análisis de Rotación (Versión PHP)

Esta es una aplicación web completa para el análisis y la predicción de la rotación de personal. La aplicación ha sido desarrollada con una arquitectura de backend en PHP y un frontend de HTML, CSS y JavaScript.

## Despliegue y Demo en Vivo

El frontend de esta aplicación se despliega automáticamente en GitHub Pages. Puedes ver una **demostración en vivo** aquí:

[**https://mmogrovejoca.github.io/people-analytics-feature/web_app/frontend/index.html**](https://mmogrovejoca.github.io/people-analytics-feature/web_app/frontend/index.html)

**Nota Importante sobre la Demo:** La demostración en vivo utiliza **datos de ejemplo locales** y no está conectada a un backend de PHP en tiempo real. Funcionalidades como la carga de archivos están deshabilitadas en este modo. Para utilizar la aplicación con todas sus capacidades, necesitas desplegar el backend por separado y conectar el frontend a él.

---

## Cómo Conectar a un Backend Real

1.  **Desplegar el Backend:**
    -   El backend de PHP (ubicado en la carpeta `php_backend`) debe ser desplegado en un servidor compatible con PHP (por ejemplo, Heroku, AWS, DigitalOcean, etc.).

2.  **Configurar el Frontend:**
    -   Abre el archivo `web_app/frontend/static/js/main.js`.
    -   En la parte superior del archivo, encontrarás las siguientes variables:
        ```javascript
        const API_URL = 'http://localhost/web_app/php_backend/api';
        const USE_FALLBACK_DATA = true;
        ```
    -   Cambia `API_URL` por la URL de tu backend desplegado.
    -   Cambia `USE_FALLBACK_DATA` a `false`.

---

## Cómo Utilizar la Aplicación Localmente

(Las instrucciones para la instalación y ejecución local permanecen igual que antes)

### 1. Requisitos Previos
...
### 2. Instalación
...
### 3. Ejecución y Uso
...
