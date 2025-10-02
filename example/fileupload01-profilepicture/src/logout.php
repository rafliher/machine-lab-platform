<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: index.php");
    exit();
}

$user = $_SESSION['user'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (!empty($_FILES['profile_pic']['name'])) {
        $filename = $_FILES['profile_pic']['name'];
        move_uploaded_file($_FILES['profile_pic']['tmp_name'], "uploads/" . $filename);
        $_SESSION['user']['profile_pic'] = $filename;
    }
}

$profile_pic = "uploads/" . ($_SESSION['user']['profile_pic'] ?? 'default.png');
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Profile</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 flex items-center justify-center h-screen">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg w-96 text-white">
        <h2 class="text-2xl font-bold mb-4">Profile</h2>
        <img src="<?= $profile_pic ?>" alt="Profile Picture" class="w-24 h-24 rounded-full mx-auto border-4 border-blue-500 mb-3">
        <p><strong>Name:</strong> <?= htmlspecialchars($user['name']) ?></p>
        <p><strong>Email:</strong> <?= htmlspecialchars($user['email']) ?></p>

        <form method="POST" enctype="multipart/form-data" class="mt-4">
            <input type="file" name="profile_pic" class="w-full text-white">
            <button type="submit" class="w-full bg-blue-500 p-2 rounded mt-2">Upload</button>
        </form>

        <a href="logout.php" class="block text-center bg-red-500 p-2 mt-4 rounded">Logout</a>
    </div>
</body>
</html>
