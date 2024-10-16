<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

$host = "localhost";
$user = "root";
$pass = "";
$db = "library";

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$method = $_SERVER['REQUEST_METHOD'];
$request = explode('/', trim($_SERVER['REQUEST_URI'],'/'));
// Remove 'api' from the beginning of the request array
array_shift($request);
$table = $request[0];

switch ($method) {
    case 'GET':
        if (isset($request[1])) {
            $id = $request[1];
            $sql = "SELECT * FROM $table WHERE id = $id";
        } else {
            $sql = "SELECT * FROM $table";
        }
        $result = $conn->query($sql);
        $data = [];
        while ($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;
    case 'POST':
        $data = json_decode(file_get_contents("php://input"), true);
        $columns = implode(", ", array_keys($data));
        $values = "'" . implode("', '", array_values($data)) . "'";
        $sql = "INSERT INTO $table ($columns) VALUES ($values)";
        if ($conn->query($sql)) {
            $data['id'] = $conn->insert_id;
            echo json_encode($data);
        } else {
            http_response_code(400);
            echo json_encode(["message" => "Failed to create record"]);
        }
        break;
    case 'PUT':
        $id = $request[1];
        $data = json_decode(file_get_contents("php://input"), true);
        $set = [];
        foreach ($data as $key => $value) {
            $set[] = "$key = '$value'";
        }
        $set = implode(", ", $set);
        $sql = "UPDATE $table SET $set WHERE id = $id";
        if ($conn->query($sql)) {
            echo json_encode(["message" => "Record updated successfully"]);
        } else {
            http_response_code(400);
            echo json_encode(["message" => "Failed to update record"]);
        }
        break;
    case 'DELETE':
        $id = $request[1];
        $sql = "DELETE FROM $table WHERE id = $id";
        if ($conn->query($sql)) {
            echo json_encode(["message" => "Record deleted successfully"]);
        } else {
            http_response_code(400);
            echo json_encode(["message" => "Failed to delete record"]);
        }
        break;
}

$conn->close();
?>