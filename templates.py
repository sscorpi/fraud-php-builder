from re import sub, DOTALL
from utils import SOURCE_PATH

HTACCESS = """RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.html -f
RewriteRule ^(.*)$ $1.html [NC,L] """

# Read App.php file
with open(f"{SOURCE_PATH}\\App.php", "r") as f:
    code = f.read()

HTML_SKELETON = sub(r"<!--.*?-->", "", code, flags=DOTALL)
