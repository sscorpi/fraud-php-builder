from re import sub, DOTALL

# Read App.php file
with open('C:/xampp/htdocs/App.php', 'r') as f:
    code = f.read()

HTML_SKELETON = sub(r'<!--.*?-->', '', code, flags=DOTALL)
