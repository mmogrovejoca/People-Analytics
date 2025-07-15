document.addEventListener('DOMContentLoaded', () => {
    // IMPORTANTE: Cambia esta URL por la de tu backend de PHP desplegado
    const API_URL = 'http://localhost/web_app/php_backend/api';
    const USE_FALLBACK_DATA = true; // Poner a 'false' en producción con un backend real

    // Inicializar gráficos
    const hiresTerminationsCtx = document.getElementById('hires-terminations-chart').getContext('2d');
    let hiresTerminationsChart = new Chart(hiresTerminationsCtx, {
        type: 'line',
        data: { labels: [], datasets: [] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Línea de Tiempo de Contrataciones y Bajas' } } }
    });

    const terminationReasonCtx = document.getElementById('termination-reason-chart').getContext('2d');
    let terminationReasonChart = new Chart(terminationReasonCtx, {
        type: 'bar',
        data: { labels: [], datasets: [] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Distribución de Motivos de Salida' } } }
    });

    // Inicializar filtros
    const dateRangePicker = new Lightpick({
        field: document.getElementById('date-range'),
        singleDate: false,
        onSelect: (start, end) => {
            if (start && end) {
                loadAllData();
            }
        }
    });

    const departmentFilter = document.getElementById('department-filter');

    // Cargar datos iniciales
    loadAllData();

    // Event listeners
    document.getElementById('file-upload').addEventListener('change', uploadFile);
    departmentFilter.addEventListener('change', loadAllData);
    document.getElementById('predict-btn').addEventListener('click', predictStatus);
    document.getElementById('report-btn').addEventListener('click', generateReport);

    async function uploadFile(event) {
        if (USE_FALLBACK_DATA) {
            alert("La carga de archivos está deshabilitada en el modo de demostración.");
            return;
        }
        // ... (lógica de carga como antes) ...
    }

    async function loadAllData() {
        const filters = getFilters();

        try {
            if (USE_FALLBACK_DATA) throw new Error("Usando datos de fallback");

            // Cargar métricas
            const metricsResponse = await fetch(`${API_URL}/metrics.php`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(filters)
            });
            if (!metricsResponse.ok) throw new Error('Error al cargar métricas');
            const metrics = await metricsResponse.json();
            updateMetrics(metrics.data);

            // Cargar datos de gráficos
            updateChart('hires_terminations_timeline', hiresTerminationsChart, filters);
            updateChart('termination_reason_distribution', terminationReasonChart, filters);

        } catch (error) {
            console.warn("No se pudo conectar a la API. Cargando datos de ejemplo locales.", error);
            loadFallbackData();
        }
    }

    async function loadFallbackData() {
        const response = await fetch('static/js/sample_data.json');
        const data = await response.json();
        updateMetrics(data.metrics);
        updateChartWithFallbackData(hiresTerminationsChart, 'line', data.charts.hires_terminations_timeline);
        updateChartWithFallbackData(terminationReasonChart, 'bar', data.charts.termination_reason_distribution);
    }

    function updateChartWithFallbackData(chartInstance, chartType, chartData) {
        chartInstance.data.labels = chartData.labels;
        if (chartType === 'line') {
             chartInstance.data.datasets = [
                { label: 'Contrataciones', data: chartData.hires, borderColor: 'blue', fill: false },
                { label: 'Bajas', data: chartData.terminations, borderColor: 'red', fill: false }
            ];
        } else {
             chartInstance.data.datasets = [{
                label: 'Motivos de Salida',
                data: chartData.values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }];
        }
        chartInstance.update();
    }


    async function updateChart(chartType, chartInstance, filters) {
        // ... (lógica de actualización como antes) ...
    }

    function updateMetrics(metrics) {
        // ... (lógica de actualización como antes) ...
    }

    async function predictStatus() {
        if (USE_FALLBACK_DATA) {
            const response = await fetch('static/js/sample_data.json');
            const data = await response.json();
            alert(`Estado Predicho (Demo): ${data.prediction.prediction}`);
            return;
        }
        // ... (lógica de predicción como antes) ...
    }

    function generateReport() {
        alert("La generación de reportes en PDF requiere un backend funcional.");
    }

    function getFilters() {
        // ... (lógica de filtros como antes) ...
    }
});
