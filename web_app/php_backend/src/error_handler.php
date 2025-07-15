<?php
function api_exception_handler($exception) {
    // Establecer el código de estado HTTP
    $code = $exception->getCode();
    if ($code === 0) {
        $code = 500; // Error interno del servidor por defecto
    }
    http_response_code($code);

    // Crear la respuesta de error
    $response = [
        'success' => false,
        'error' => [
            'message' => $exception->getMessage(),
            'code' => $exception->getCode()
        ]
    ];

    // Enviar la respuesta JSON y terminar el script
    echo json_encode($response);
    exit;
}
?>
