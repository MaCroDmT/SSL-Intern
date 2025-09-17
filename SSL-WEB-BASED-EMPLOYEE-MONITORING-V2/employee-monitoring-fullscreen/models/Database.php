<?php
// models/Database.php
class Database {
    private $host = "localhost";
    private $user = "root";
    private $pass = "";
    private $dbname = "employee_monitoring_fullscreen";
    public $conn;

    public function __construct() {
        $this->conn = new mysqli($this->host, $this->user, $this->pass, $this->dbname);

        if ($this->conn->connect_error) {
            die("DB Connection failed: " . $this->conn->connect_error);
        }
    }
}
