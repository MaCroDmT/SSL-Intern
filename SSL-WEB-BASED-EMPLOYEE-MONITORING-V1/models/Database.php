<?php
// models/Database.php
class Database {
    private $host = 'localhost';
    private $user = 'root';
    private $pass = '';
    private $db = 'employee_monitor';
    public $conn;

    public function __construct(){
        $this->conn = new mysqli($this->host, $this->user, $this->pass, $this->db);
        if ($this->conn->connect_error) {
            die("DB Conn failed: " . $this->conn->connect_error);
        }
        $this->conn->set_charset("utf8mb4");
    }
}
