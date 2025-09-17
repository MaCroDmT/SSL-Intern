<?php
// models/ScreenshotModel.php
require_once __DIR__ . '/Database.php';

class ScreenshotModel {
    private $db;

    public function __construct() {
        $this->db = (new Database())->conn;
    }

    public function saveScreenshot($userId, $filename, $filePath) {
        $stmt = $this->db->prepare("INSERT INTO screenshots (user_id, filename, file_path) VALUES (?,?,?)");
        $stmt->bind_param("iss", $userId, $filename, $filePath);
        return $stmt->execute();
    }

    public function getTodaysScreenshots($userId) {
        $sql = "SELECT * FROM screenshots WHERE user_id = ? AND DATE(created_at) = CURDATE() ORDER BY created_at ASC";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }

    public function updateSessionStatus($userId, $status) {
        $stmt = $this->db->prepare("INSERT INTO sessions (user_id, status) VALUES (?, ?) 
                                    ON DUPLICATE KEY UPDATE status = VALUES(status)");
        $stmt->bind_param("is", $userId, $status);
        return $stmt->execute();
    }

    public function getSessionStatus($userId) {
        $stmt = $this->db->prepare("SELECT status FROM sessions WHERE user_id = ? ORDER BY id DESC LIMIT 1");
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        $res = $stmt->get_result()->fetch_assoc();
        return $res ? $res['status'] : "stopped";
    }
}
