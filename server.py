from os import chdir
from os.path import isdir, join, splitext
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

PORT = 8000


class RequestHandler(SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        """Override log_request to print the requested URL."""
        url = f"http://localhost:{PORT}{self.path}"
        print(f"Request: {url}")

    def translate_path(self, path):
        """Override translate_path to append .html to requested paths."""
        # get the default translated path
        path = super().translate_path(path)

        # check if the path is a directory
        if isdir(path):
            # append the default index file name
            path = join(path, 'index.html')

        # append .html to the path if it has no file extension
        if not splitext(path)[1]:
            path += '.html'

        return path


def start_server():
    print(f"Serving at http://localhost:{PORT}")
    # change the current working directory to build/
    chdir("build/")

    Handler = RequestHandler

    httpd = TCPServer(("", PORT), Handler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")
