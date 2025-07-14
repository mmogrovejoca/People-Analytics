<?php
require 'vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\IOFactory;

function load_data($filepath) {
    $fileType = IOFactory::identify($filepath);
    $reader = IOFactory::createReader($fileType);
    $spreadsheet = $reader->load($filepath);
    $data = $spreadsheet->getActiveSheet()->toArray(null, true, true, true);

    // Convertir a un array asociativo
    $header = array_shift($data);
    $assocData = [];
    foreach ($data as $row) {
        $assocData[] = array_combine($header, $row);
    }

    return $assocData;
}

function preprocess_data($data) {
    if (!$data) {
        return null;
    }

    foreach ($data as &$row) {
        $ingreso = new DateTime($row['FECHA_INGRESO']);
        $salida = $row['FECHA_SALIDA'] ? new DateTime($row['FECHA_SALIDA']) : null;

        $row['FECHA_INGRESO_DT'] = $ingreso;
        $row['FECHA_SALIDA_DT'] = $salida;

        $hoy = new DateTime();
        $fecha_final = $salida ?? $hoy;
        $diferencia = $fecha_final->diff($ingreso);
        $row['DURACION_EMPLEO'] = $diferencia->days;

        $row['MES_INGRESO'] = (int)$ingreso->format('m');
        $row['ANIO_INGRESO'] = (int)$ingreso->format('Y');
        $row['MES_SALIDA'] = $salida ? (int)$salida->format('m') : null;
        $row['ANIO_SALIDA'] = $salida ? (int)$salida->format('Y') : null;
    }

    return $data;
}
?>
