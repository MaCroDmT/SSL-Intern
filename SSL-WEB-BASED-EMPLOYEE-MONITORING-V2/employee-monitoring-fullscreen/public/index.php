<?php
// public/index.php
require_once __DIR__ . '/../controllers/ScreenshotController.php';

$controller = new ScreenshotController();

if (isset($_GET['action'])) {
    $action = $_GET['action'];
    if (in_array($action, ['started','paused','stopped'])) {
        $controller->setStatus($action);
    } elseif ($action === 'save') {
        $controller->save();   // <-- NEW
    } else {
        echo "Invalid action";
    }
} else {
    require_once __DIR__ . '/../views/home.php';
}
