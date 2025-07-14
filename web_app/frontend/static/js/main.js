document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1/web_app/php_backend/api'; // Asumiendo un servidor web local

    // Inicializar gráficos
    const hiresTerminationsCtx = document.getElementById('hires-terminations-chart').getContext('2d');
    const hiresTerminationsChart = new Chart(hiresTerminationsCtx, {
        type: 'line',
        data: { labels: [], datasets: [] },
        options: { responsive: true, maintainAspectRatio: false }
    });

    const terminationReasonCtx = document.getElementById('termination-reason-chart').getContext('2d');
    const terminationReasonChart = new Chart(terminationReasonCtx, {
        type: 'bar',
        data: { labels: [], datasets: [] },
        options: { responsive: true, maintainAspectRatio: false }
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
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            loadAllData();
        } else {
            alert(`Error: ${result.error}`);
        }
    }

    async function loadAllData() {
        const filters = getFilters();

        // Cargar métricas
        const metricsResponse = await fetch(`${API_URL}/metrics.php`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
        const metrics = await metricsResponse.json();
        updateMetrics(metrics);

        // Cargar datos de gráficos
        updateChart('hires_terminations_timeline', hiresTerminationsChart, filters);
        // updateChart('termination_reason_distribution', terminationReasonChart, filters); // Pendiente
    }

    async function updateChart(chartType, chartInstance, filters) {
        const response = await fetch(`${API_URL}/chart-data.php`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...filters, chart_type: chartType })
        });
        const data = await response.json();

        if (chartType === 'hires_terminations_timeline') {
            chartInstance.data.labels = data.labels;
            chartInstance.data.datasets = [
                { label: 'Contrataciones', data: data.hires, borderColor: 'blue', fill: false },
                { label: 'Bajas', data: data.terminations, borderColor: 'red', fill: false }
            ];
        } else if (chartType === 'termination_reason_distribution') {
            chartInstance.data.labels = data.labels;
            chartInstance.data.datasets = [{
                label: 'Motivos de Salida',
                data: data.values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }];
        }
        chartInstance.update();
    }

    function updateMetrics(metrics) {
        const container = document.getElementById('metrics-container');
        container.innerHTML = `
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${metrics.total_hires}</h5>
                        <p class="card-text">Total Contrataciones</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${metrics.total_terminations}</h5>
                        <p class="card-text">Total Bajas</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${metrics.retention_rate} %</h5>
                        <p class="card-text">Tasa de Retención Anual</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${metrics.average_tenure.toFixed(2)}</h5>
                        <p class="card-text">Antigüedad Promedio (días)</p>
                    </div>
                </div>
            </div>
        `;
    }

    async function predictStatus() {
        // La predicción ahora se hace con un script de python llamado desde php
        const response = await fetch(`${API_URL}/predict.php`, {
            method: 'GET' // No se necesitan filtros, usa la sesión
        });
        const result = await response.json();
        alert(`Estado Predicho: ${result.prediction}`);
    }

    async function generateReport() {
        // La generación de reportes en PDF desde PHP es compleja y se omite en esta fase
        alert("La generación de reportes en PDF no está implementada en la versión PHP.");
        return;

        const filters = getFilters();
        const response = await fetch(`${API_URL}/report.php`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'reporte_rotacion.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    }

    function getFilters() {
        const [start, end] = dateRangePicker.getDates();
        const departments = Array.from(departmentFilter.selectedOptions).map(opt => opt.value);
        return {
            start_date: start ? start.format('YYYY-MM-DD') : null,
            end_date: end ? end.format('YYYY-MM-DD') : null,
            departments: departments
        };
    }
});
