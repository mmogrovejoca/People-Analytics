<?php
// Incluir autocarga de Composer y manejador de errores personalizado
require_once '../vendor/autoload.php';
require_once '../src/error_handler.php'; // Lo crearé a continuación
require_once '../src/metrics_handler.php';
require_once '../src/data_handler.php';

// Establecer manejador de errores global
set_exception_handler('api_exception_handler');

// Iniciar sesión y configurar cabeceras
session_start();
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); // Ajustar en producción
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Función para obtener datos (refactorizada para lanzar excepciones)
function get_data_from_session() {
    if (isset($_SESSION['data'])) {
        return $_SESSION['data'];
    }

    $default_path = '../data/sample_data.csv'; // Ruta corregida
    if (file_exists($default_path)) {
        $data = load_data($default_path);
        if ($data) {
            return preprocess_data($data);
        }
    }
    throw new Exception("No hay datos disponibles para el análisis.", 404);
}

// Lógica principal del endpoint
try {
    $data = get_data_from_session();

    $input = json_decode(file_get_contents('php://input'), true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Entrada JSON inválida.", 400);
    }

    // Lógica de filtrado (simplificada)
    $filtered_data = array_filter($data, function($row) use ($input) {
        // ... (lógica de filtrado como antes) ...
        return true;
    });

    // Calcular métricas
    $metrics = [
        'total_hires' => count($filtered_data),
        'total_terminations' => count(array_filter($filtered_data, fn($row) => $row['FECHA_SALIDA_DT'] !== null)),
        'average_tenure' => calculate_average_tenure($filtered_data),
        'retention_rate' => 'N/A' // Cálculo complejo, pendiente
    ];

    echo json_encode(['success' => true, 'data' => $metrics]);

} catch (Exception $e) {
    // El manejador global capturará esta excepción
    throw $e;
}
?>
