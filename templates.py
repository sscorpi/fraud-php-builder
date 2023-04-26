from re import sub, DOTALL

HTACCESS = """RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.html -f
RewriteRule ^(.*)$ $1.html [NC,L] """

# Read App.php file
with open("C:/xampp/htdocs/App.php", "r") as f:
    code = f.read()

HTML_SKELETON = sub(r"<!--.*?-->", "", code, flags=DOTALL)
