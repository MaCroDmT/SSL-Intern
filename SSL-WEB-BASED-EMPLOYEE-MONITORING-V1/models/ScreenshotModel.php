<?php
// models/ScreenshotModel.php
require_once __DIR__ . '/Database.php';

class ScreenshotModel {
    private $db;

    public function __construct() {
        $database = new Database();
        $this->db = $database->conn;
    }

    public function saveScreenshot($userId, $filename, $filePath) {
        $stmt = $this->db->prepare("INSERT INTO screenshots (user_id, filename, file_path) VALUES (?, ?, ?)");
        $stmt->bind_param("iss", $userId, $filename, $filePath);
        $ok = $stmt->execute();
        $stmt->close();
        return $ok;
    }

    public function getUserScreenshots($userId) {
    // Keep connection alive
    if (!$this->db->ping()) {
        $this->db->close();
        $database = new Database();
        $this->db = $database->conn;
    }

    $stmt = $this->db->prepare("SELECT * FROM screenshots WHERE user_id = ? ORDER BY created_at ASC");
    $stmt->bind_param("i", $userId);
    $stmt->execute();
    $res = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    $stmt->close();
    return $res;
}


    public function deleteUserScreenshots($userId) {
        $stmt = $this->db->prepare("DELETE FROM screenshots WHERE user_id = ?");
        $stmt->bind_param("i", $userId);
        $ok = $stmt->execute();
        $stmt->close();
        return $ok;
    }
}
