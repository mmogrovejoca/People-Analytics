<?php
function calculate_average_tenure($data) {
    if (empty($data)) {
        return 0;
    }

    $total_duration = 0;
    foreach ($data as $row) {
        $total_duration += $row['DURACION_EMPLEO'];
    }

    return $total_duration / count($data);
}

// Aquí se añadirían las demás funciones de cálculo de métricas...
?>
