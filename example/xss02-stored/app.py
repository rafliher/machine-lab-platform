from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from datetime import datetime
import sqlite3
import os
import sys
import logging

app = Flask(__name__)
app.secret_key = 'xss_stored_secret_key_2024'

# Configure logging to ensure output appears in Docker logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add some default comments
    cursor.execute("SELECT COUNT(*) FROM comments")
    if cursor.fetchone()[0] == 0:
        default_comments = [
            ("Admin", "Welcome to our comment system! Feel free to leave your thoughts."),
            ("Alice", "This is a great website!"),
            ("Bob", "I love the new features you've added.")
        ]
        cursor.executemany("INSERT INTO comments (name, comment) VALUES (?, ?)", default_comments)
        conn.commit()
    
    conn.close()

# Exploit server to capture XSS payloads
class ExploitHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the request
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Log the request
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'path': self.path,
            'query_params': query_params,
            'user_agent': self.headers.get('User-Agent', ''),
            'referer': self.headers.get('Referer', ''),
            'cookie': self.headers.get('Cookie', '')
        }
        
        # Save to exploit log
        with open('exploit_log.txt', 'a') as f:
            f.write(json.dumps(log_data) + '\n')
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_html = f'''
        <html>
        <head><title>Exploit Server</title></head>
        <body>
            <h1>Exploit Server</h1>
            <p>Request logged successfully!</p>
            <p>Check the exploit log for captured data.</p>
            <script>
                // Auto-close if opened in popup
                if (window.opener) {{
                    window.close();
                }}
            </script>
        </body>
        </html>
        '''
        self.wfile.write(response_html.encode())
    
    def do_POST(self):
        self.do_GET()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_exploit_server():
    try:
        server = HTTPServer(('0.0.0.0', 8080), ExploitHandler)
        logger.info("Exploit server running on http://localhost:8080")
        sys.stdout.flush()
        server.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            logger.info("Exploit server port 8080 already in use - skipping startup")
        else:
            logger.error(f"Exploit server error: {e}")
        sys.stdout.flush()

@app.route('/')
def index():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, comment, timestamp FROM comments ORDER BY timestamp DESC")
    comments = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    name = request.form.get('name', '').strip()
    comment = request.form.get('comment', '').strip()
    
    if not name or not comment:
        flash('Name and comment are required!', 'error')
        return redirect(url_for('index'))
    
    # Store comment without sanitization (vulnerable to XSS)
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (name, comment) VALUES (?, ?)", (name, comment))
    conn.commit()
    conn.close()
    
    flash('Comment added successfully!', 'success')
    
    # Simulate admin viewing the comments after 3 seconds
    logger.info(f"Comment added by '{name}'. Admin will visit in 3 seconds...")
    sys.stdout.flush()
    threading.Timer(3.0, simulate_admin_visit).start()
    
    return redirect(url_for('index'))

def simulate_admin_visit():
    """Simulate admin visiting the page with stored XSS"""
    logger.info("=== Starting admin simulation ===")
    sys.stdout.flush()
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        import os
        
        # Get Selenium URL from environment or use default
        selenium_url = os.environ.get('SELENIUM_URL', 'http://selenium:4444')
        logger.info(f"Using Selenium URL: {selenium_url}")
        sys.stdout.flush()
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')  # Allow cross-origin requests
        chrome_options.add_argument('--allow-running-insecure-content')  # Allow mixed content
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Use remote WebDriver
        logger.info("Creating WebDriver connection...")
        sys.stdout.flush()
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=chrome_options
        )
        
        logger.info("WebDriver connected successfully!")
        logger.info("Setting admin cookies...")
        sys.stdout.flush()
        
        # Set admin session using Docker service name
        driver.get('http://server/admin_login')
        time.sleep(2)
        
        # Print current cookies after admin login
        cookies = driver.get_cookies()
        logger.info(f"Admin cookies set: {cookies}")
        sys.stdout.flush()
        
        # Visit main page as admin (this will trigger stored XSS)
        logger.info("Admin visiting main page...")
        sys.stdout.flush()
        driver.get('http://server/')
        
        # Get page source to debug
        page_source = driver.page_source
        logger.info(f"Page loaded, title: {driver.title}")
        logger.info(f"Page source length: {len(page_source)} characters")
        
        # Check if there are any JavaScript errors
        try:
            logs = driver.get_log('browser')
            if logs:
                logger.info(f"Browser console logs: {logs}")
            else:
                logger.info("No browser console logs found")
        except Exception as log_error:
            logger.warning(f"Could not get browser logs: {log_error}")
        
        sys.stdout.flush()
        
        # Wait longer and check for any network requests
        logger.info("Waiting for XSS to execute...")
        sys.stdout.flush()
        time.sleep(10)  # Increased wait time
        
        # Check cookies again to see if they're still there
        final_cookies = driver.get_cookies()
        logger.info(f"Final cookies: {final_cookies}")
        sys.stdout.flush()
        
        driver.quit()
        logger.info("=== Admin simulation completed successfully ===")
        sys.stdout.flush()
        
    except ImportError:
        logger.error("Selenium not available for admin simulation")
        sys.stdout.flush()
    except Exception as e:
        logger.error(f"Admin simulation error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        sys.stdout.flush()

@app.route('/admin_login')
def admin_login():
    # Check if request is from bot/selenium (internal access only)
    user_agent = request.headers.get('User-Agent', '')
    referer = request.headers.get('Referer', '')
    
    # Only allow access from selenium/bot or internal Docker network
    if not ('selenium' in user_agent.lower() or 
            'headless' in user_agent.lower() or
            request.remote_addr.startswith('172.') or  # Docker network
            request.remote_addr == '127.0.0.1'):
        return "Access denied. This endpoint is for internal use only.", 403
    
    # Simulate admin login
    session['admin'] = True
    session['username'] = 'admin'
    
    # Create response and set cookies that can be stolen via XSS
    response = make_response("Admin logged in (simulation)")
    response.set_cookie('admin_session', 'true', httponly=False)  # httponly=False makes it accessible to JavaScript
    response.set_cookie('username', 'admin', httponly=False)
    response.set_cookie('flag', 'AKAMSI{st0r3d_xss_c4n_st34l_c00k13s_4nd_s3ss10ns}', httponly=False)
    
    return response

@app.route('/exploit_server')
def exploit_server_page():
    # Read exploit log
    exploit_logs = []
    if os.path.exists('exploit_log.txt'):
        with open('exploit_log.txt', 'r') as f:
            for line in f:
                try:
                    exploit_logs.append(json.loads(line.strip()))
                except:
                    pass
    
    return render_template('exploit_server.html', logs=exploit_logs)

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    if os.path.exists('exploit_log.txt'):
        os.remove('exploit_log.txt')
    flash('Exploit logs cleared!', 'success')
    return redirect(url_for('exploit_server_page'))

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start exploit server in background
    exploit_thread = threading.Thread(target=start_exploit_server, daemon=True)
    exploit_thread.start()
    
    # Check if running in Docker to avoid debug mode issues
    is_docker = os.path.exists('/.dockerenv')
    debug_mode = not is_docker  # Only enable debug when not in Docker
    
    # Start Flask app
    app.run(host='0.0.0.0', port=80, debug=debug_mode)