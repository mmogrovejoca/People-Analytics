<?php
session_start();
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once '../src/metrics_handler.php'; // Lo crearé a continuación

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

if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'No hay datos disponibles.']);
    exit;
}

$filters = json_decode(file_get_contents('php://input'), true);

// Lógica de filtrado (simplificada)
$filtered_data = array_filter($data, function($row) use ($filters) {
    $ingreso_date = $row['FECHA_INGRESO_DT'];
    $start_date = isset($filters['start_date']) ? new DateTime($filters['start_date']) : null;
    $end_date = isset($filters['end_date']) ? new DateTime($filters['end_date']) : null;

    if ($start_date && $ingreso_date < $start_date) return false;
    if ($end_date && $ingreso_date > $end_date) return false;
    if (!empty($filters['departments']) && !in_array($row['AREA'], $filters['departments'])) return false;

    return true;
});

// Calcular métricas
$total_hires = count($filtered_data);
$total_terminations = count(array_filter($filtered_data, fn($row) => $row['FECHA_SALIDA_DT'] !== null));
$average_tenure = calculate_average_tenure($filtered_data); // Implementar en metrics_handler

$metrics = [
    'total_hires' => $total_hires,
    'total_terminations' => $total_terminations,
    'average_tenure' => $average_tenure,
    'retention_rate' => 'N/A' // Cálculo complejo, pendiente
];

echo json_encode($metrics);
?>
