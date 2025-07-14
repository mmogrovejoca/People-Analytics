<?php
session_start();
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// (Lógica para obtener y filtrar datos similar a metrics.php)
function get_data_from_session() {
    if (isset($_SESSION['data'])) {
        return $_SESSION['data'];
    }
    // Lógica para cargar datos por defecto si no hay sesión
    require_once '../src/data_handler.php';
    $default_path = '../../backend/data/sample_data.csv'; // Ajustar ruta
    if (file_exists($default_path)) {
        $data = load_data($default_path);
        return preprocess_data($data);
    }
    return null;
}

$data = get_data_from_session();
$filters = json_decode(file_get_contents('php://input'), true);
$chart_type = $filters['chart_type'] ?? '';

// (Lógica de filtrado)
$filtered_data = array_filter($data, function($row) use ($filters) {
    $ingreso_date = $row['FECHA_INGRESO_DT'];
    $start_date = isset($filters['start_date']) ? new DateTime($filters['start_date']) : null;
    $end_date = isset($filters['end_date']) ? new DateTime($filters['end_date']) : null;

    if ($start_date && $ingreso_date < $start_date) return false;
    if ($end_date && $ingreso_date > $end_date) return false;
    if (!empty($filters['departments']) && !in_array($row['AREA'], $filters['departments'])) return false;

    return true;
});


if ($chart_type === 'hires_terminations_timeline') {
    // Lógica para agrupar por mes (simplificada)
    $hires_by_month = [];
    $terminations_by_month = [];

    foreach ($filtered_data as $row) {
        $month_year = $row['FECHA_INGRESO_DT']->format('Y-m');
        if (!isset($hires_by_month[$month_year])) {
            $hires_by_month[$month_year] = 0;
        }
        $hires_by_month[$month_year]++;

        if ($row['FECHA_SALIDA_DT']) {
            $month_year_term = $row['FECHA_SALIDA_DT']->format('Y-m');
            if (!isset($terminations_by_month[$month_year_term])) {
                $terminations_by_month[$month_year_term] = 0;
            }
            $terminations_by_month[$month_year_term]++;
        }
    }

    ksort($hires_by_month);
    ksort($terminations_by_month);

    // Unir claves para el eje X
    $labels = array_keys(array_merge($hires_by_month, $terminations_by_month));
    sort($labels);

    $hires_data = array_map(fn($l) => $hires_by_month[$l] ?? 0, $labels);
    $terminations_data = array_map(fn($l) => $terminations_by_month[$l] ?? 0, $labels);

    echo json_encode([
        'labels' => $labels,
        'hires' => $hires_data,
        'terminations' => $terminations_data
    ]);
}
// Añadir otros tipos de gráficos aquí...
else {
    http_response_code(404);
    echo json_encode(['error' => 'Chart type not found']);
}
?>
