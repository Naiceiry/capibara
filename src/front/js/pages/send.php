<?php
error_reporting(0);
$nombre = $_POST['nombre'];
$correo= $_POST['correo'];
$telefono = $_POST['telefono'];

$Pais=$_POST['Pais'];
$Provincia=$_POST['Provincia'];
$Ciudad= $_POST['Ciudad'];
$CodigoPostal=$_POST['CodigoPostal'];

$Paisd=$_POST['Paisd'];
$Provinciad=$_POST['Provinciad'];
$Ciudadd= $_POST['Ciudadd'];
$CodigoPostald=$_POST['CodigoPostald'];

$header = 'From: ' . $correo . "\r\n";
$header .= "X-Mailer: PHP/" . phpversion() . " \r\n";
$header .= "Mime-Version: 1.0 \r\n";
$header .= "Content-Type: text/plain";

$mensaje = "Este mensaje fue enviado por " . $nombre . " \r\n";
$mensaje .= "Su e-mail es: " . $correo . " \r\n";
$mensaje .= "Telefono" . $_POST['telefono'] . " \r\n";
$mensaje .= "Descripcion de la Mudanza"  " \r\n";
$mensaje .= "Origen"  " \r\n";
$mensaje .="Pais".$_POST['Pais'] . " \r\n";
$mensaje .="Provincia".$_POST['Provincia'] . " \r\n";
$mensaje .="Ciudad".$_POST['Ciudad'] . " \r\n";
$mensaje .="CodigoPostal".$_POST['CodigoPostal'] . " \r\n";
$mensaje .= " \r\n";
$mensaje .= "Destino"  " \r\n";
$mensaje .="Paisd".$_POST['Paisd'] . " \r\n";
$mensaje .="Provinciad".$_POST['Provinciad'] . " \r\n";
$mensaje .="Ciudadd".$_POST['Ciudadd'] . " \r\n";
$mensaje .="CodigoPostald".$_POST['CodigoPostald'] . " \r\n";
$mensaje .= "Enviado el " . date('d/m/Y', time());

$para = capibaraportesymudanzas@gmail.com;
$asunto = 'Nueva solicitud de presupuesto';

mail($para, $asunto, utf8_decode($mensaje), $header);

echo 'mensaje enviado correctamente';

?>
