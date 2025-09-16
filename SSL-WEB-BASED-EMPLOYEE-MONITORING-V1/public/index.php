<?php
require_once __DIR__ . '/../controllers/ScreenshotController.php';
$ctrl = new ScreenshotController();

$action = isset($_GET['action']) ? $_GET['action'] : '';
if ($action === 'save') {
    $ctrl->save();
} else if ($action === 'download') {
    $ctrl->downloadZip();
} else {
    // Show home (view)
    header("Location: ../views/home.php");
}
