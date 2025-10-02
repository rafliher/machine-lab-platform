# fileupload01-profilepicture

## Nama Challenge
**File Upload Vulnerability - Profile Picture**

## Deskripsi
Challenge ini mendemonstrasikan kerentanan file upload dalam aplikasi web yang memungkinkan pengguna untuk mengunggah foto profil. Aplikasi gagal untuk memvalidasi jenis file, ukuran, dan konten dengan benar, memungkinkan penyerang untuk mengunggah file berbahaya yang dapat menyebabkan remote code execution.

Fitur aplikasi:
- Sistem manajemen profil berbasis PHP
- Fungsi file upload untuk foto profil
- Validasi file yang tidak memadai
- Akses langsung ke file yang diunggah
- Tidak ada pembatasan jenis file atau filtering konten

## Tujuan
Eksploitasi kerentanan file upload untuk mengunggah file berbahaya dan mendapatkan remote code execution pada server.

## Flag
`AKAMSI{file_upload_rce_is_critical}`

## Akses
- **Port**: 5008
- **URL**: http://localhost:5008

## Petunjuk
- Coba unggah file PHP alih-alih gambar
- Direktori uploads mungkin dapat diakses secara langsung
- Validasi ekstensi file mungkin lemah atau tidak ada
- Cari cara untuk bypass pemeriksaan jenis file
- Coba ekstensi file yang berbeda: .php, .phtml, .php5
- Periksa direktori uploads/ untuk file yang Anda unggah

## File yang Menarik
- `index.php` - Halaman login/registrasi
- `profile.php` - Manajemen profil dengan fungsi upload
- `uploads/` - Direktori tempat file yang diunggah disimpan
- Berbagai file yang diunggah yang mungkin berisi shell