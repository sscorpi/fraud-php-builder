from re import sub, DOTALL

HTACCESS = """php_value display_errors Off
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.php -f
RewriteRule ^(.*)$ $1.php [NC,L]"""

# Read App.php file
with open('C:/xampp/htdocs/App.php', 'r') as f:
    code = f.read()

HTML_SKELETON = sub(r'<!--.*?-->', '', code, flags=DOTALL)
