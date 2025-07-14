<?php
session_start();
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once '../src/data_handler.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $uploadDir = '../uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    $uploadFile = $uploadDir . basename($_FILES['file']['name']);

    if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
        try {
            $data = load_data($uploadFile);
            $processed_data = preprocess_data($data);
            $_SESSION['data'] = $processed_data;
            echo json_encode(['message' => 'Archivo subido y procesado correctamente']);
        } catch (Exception $e) {
            http_response_code(500);
            echo json_encode(['error' => 'Error al procesar el archivo: ' . $e->getMessage()]);
        }
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Error al subir el archivo.']);
    }
} else {
    http_response_code(400);
    echo json_encode(['error' => 'No se ha subido ningún archivo.']);
}
?>
