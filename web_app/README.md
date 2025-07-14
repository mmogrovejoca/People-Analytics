# People Analytics: Aplicación Web de Análisis de Rotación (Versión PHP)

Esta es una aplicación web completa para el análisis y la predicción de la rotación de personal. La aplicación ha sido desarrollada con una arquitectura de backend en PHP y un frontend de HTML, CSS y JavaScript.

**Nota Importante:** Esta versión utiliza un backend en PHP. Debido a las limitaciones de PHP para la ciencia de datos, algunas funcionalidades (como la generación de reportes en PDF y ciertos gráficos avanzados) han sido simplificadas u omitidas en comparación con una versión con backend en Python.

## Características Principales

- **Dashboard Interactivo:** Visualiza las métricas clave de rotación.
- **Carga de Datos:** Sube tus propios datos en formato CSV o Excel.
- **Filtros Dinámicos:** Filtra los datos por rango de fechas y departamento.
- **Visualizaciones Claras:** Gráficos interactivos para entender las tendencias.
- **Predicción de Estado:** Utiliza un modelo de Machine Learning (a través de un script de Python) para predecir el estado futuro de la empresa.

## Estructura del Proyecto

- `php_backend/`: Contiene la lógica del backend desarrollada con PHP.
  - `api/`: Endpoints de la API.
  - `src/`: Lógica de negocio (manejo de datos, métricas).
  - `uploads/`: Directorio para los archivos subidos.
  - `vendor/`: Dependencias de Composer.
  - `predict.py`: Script de Python para las predicciones.
  - `composer.json`: Dependencias de PHP.
- `frontend/`: Contiene los archivos del frontend.
  - `static/`: Archivos estáticos (CSS, JavaScript).
  - `templates/`: Plantillas HTML (aunque se sirven desde el backend, están aquí por organización).
- `requirements.txt`: Dependencias de Python para el script de predicción.
- `README.md`: Este archivo.

## Cómo Utilizar la Aplicación

### 1. Requisitos Previos

- **Servidor Web Local:** Necesitas un servidor web local con soporte para PHP, como Apache o Nginx (XAMPP, WAMP, MAMP son buenas opciones).
- **PHP:** Versión 7.4 o superior.
- **Composer:** El gestor de dependencias para PHP.
- **Python 3:** Con `pip` para instalar las dependencias del script de predicción.

### 2. Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd web_app
    ```

2.  **Configurar el Backend de PHP:**
    -   Navega al directorio `php_backend`:
        ```bash
        cd php_backend
        ```
    -   Instala las dependencias de PHP con Composer:
        ```bash
        composer install
        ```

3.  **Configurar el Script de Python:**
    -   Navega de nuevo al directorio raíz `web_app`.
    -   Instala las dependencias de Python:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configurar el Servidor Web:**
    -   Copia o enlaza el directorio `web_app` a la raíz de tu servidor web (por ejemplo, `htdocs` en XAMPP).
    -   Asegúrate de que tu servidor web esté en funcionamiento.

### 3. Ejecución y Uso

1.  **Abrir la Aplicación:**
    -   Abre tu navegador web y navega a la URL correspondiente a la ubicación del proyecto en tu servidor local. Por ejemplo:
        ```
        http://localhost/web_app/
        ```
    -   Deberías ver el dashboard principal.

2.  **Cargar Datos:**
    -   En la barra lateral, utiliza el campo "Cargar Archivo" para subir un archivo CSV o Excel con tus datos de empleados.
    -   Una vez subido, el dashboard se actualizará automáticamente con tus datos.

3.  **Utilizar los Filtros:**
    -   Selecciona un rango de fechas y/o uno o más departamentos en la barra lateral para filtrar los datos.
    -   Las métricas y los gráficos se actualizarán para reflejar tu selección.

4.  **Realizar Predicciones:**
    -   Haz clic en el botón "Predecir Estado" para obtener una predicción del estado de la empresa. La predicción se basará en los datos actualmente cargados y filtrados.

5.  **Nota sobre el Modelo:**
    -   El sistema utiliza un modelo de Machine Learning pre-entrenado (`model.joblib`). Si deseas re-entrenar el modelo con tus propios datos, necesitarás ejecutar los notebooks de Jupyter del proyecto original (en la versión de Python).
