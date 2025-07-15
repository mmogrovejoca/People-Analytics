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

## Guía de Uso de la Aplicación (Local o Conectada)

Una vez que tengas la aplicación funcionando (ya sea localmente o conectada a un backend real), sigue estos pasos para utilizarla:

### Paso 1: Cargar tus Datos

-   En la barra lateral izquierda, verás una sección llamada **"Carga de Datos"**.
-   Haz clic en el botón "Seleccionar archivo" y elige un archivo de tu computadora.
-   El sistema es compatible con archivos **CSV (.csv)** y **Excel (.xlsx)**.
-   **Importante:** La carga de archivos solo funcionará si estás ejecutando la aplicación localmente o conectada a un backend real (no en la demo de GitHub Pages).
-   Una vez que subas el archivo, el dashboard se actualizará automáticamente con tus datos. Si no subes ningún archivo, la aplicación utilizará un conjunto de datos de ejemplo por defecto.

### Paso 2: Filtrar y Explorar

-   Justo debajo de la carga de datos, se encuentra la sección de **"Filtros"**.
-   **Rango de Fechas:** Haz clic en el campo de fecha para abrir un calendario y selecciona un rango de fechas para analizar las contrataciones dentro de ese período.
-   **Departamento:** Selecciona uno o más departamentos de la lista para filtrar los datos y centrarte en áreas específicas de la empresa.
-   Cada vez que cambies un filtro, todas las métricas y gráficos en el dashboard se actualizarán en tiempo real.

### Paso 3: Analizar las Métricas y Gráficos

-   **Dashboard Principal:** El área principal de la página te mostrará:
    -   **Tarjetas de Métricas:** Un resumen rápido del total de contrataciones, bajas, tasa de retención y antigüedad promedio.
    -   **Gráficos:** Visualizaciones interactivas como la línea de tiempo de contrataciones y bajas, y la distribución de los motivos de salida.

### Paso 4: Realizar Predicciones

-   En la barra lateral, en la sección de **"Acciones"**, encontrarás el botón **"Predecir Estado"**.
-   Haz clic en este botón para que el modelo de Machine Learning analice los datos (según los filtros que hayas aplicado) y prediga el estado de la empresa para el próximo período.
-   Se mostrará una alerta con el resultado de la predicción (por ejemplo, "Estable", "En Expansión", etc.).

### Paso 5: Generar Reportes

-   El botón **"Generar Reporte PDF"** (deshabilitado en la versión PHP de la demo) te permitiría descargar un resumen en PDF de los datos y gráficos actuales.

---

## Cómo Utilizar la Aplicación Localmente

(Las instrucciones para la instalación y ejecución local permanecen igual que antes)
...
