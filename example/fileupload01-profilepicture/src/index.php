<?php
session_start();
if (isset($_SESSION['user'])) {
    header("Location: profile.php");
    exit();
}
$error = '';
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'] ?? '';
    $email = $_POST['email'] ?? '';
    
    if (!empty($name) && !empty($email)) {
        $_SESSION['user'] = ['name' => $name, 'email' => $email, 'profile_pic' => 'default.png'];
        header("Location: profile.php");
        exit();
    } else {
        $error = "All fields are required!";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 flex items-center justify-center h-screen">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h2 class="text-2xl font-bold text-white mb-4">Login</h2>
        <?php if ($error): ?>
            <p class="text-red-500"><?= $error ?></p>
        <?php endif; ?>
        <form method="POST">
            <input type="text" name="name" placeholder="Name" class="w-full p-2 mb-3 rounded bg-gray-700 text-white">
            <input type="email" name="email" placeholder="Email" class="w-full p-2 mb-3 rounded bg-gray-700 text-white">
            <button type="submit" class="w-full bg-blue-500 p-2 rounded text-white">Login</button>
        </form>
    </div>
</body>
</html>
