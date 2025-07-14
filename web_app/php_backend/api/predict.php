<?php
session_start();
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

function get_data_from_session() {
    if (isset($_SESSION['data'])) {
        return $_SESSION['data'];
    }
    return null;
}

$data = get_data_from_session();

if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'No hay datos disponibles.']);
    exit;
}

// Convertir los datos a JSON para pasarlos al script de Python
$data_json = json_encode($data);

// Escapar el string JSON para pasarlo como argumento de línea de comandos
$escaped_data_json = escapeshellarg($data_json);

// Llamar al script de Python
$command = "python ../predict.py " . $escaped_data_json;
$output = shell_exec($command);

// Devolver la salida del script de Python
echo $output;
?>
