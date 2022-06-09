from http.server import BaseHTTPRequestHandler, HTTPServer
from infrastructure.web_server import HttpServer

if __name__ == "__main__":
    web_server = HTTPServer(("localhost", 8080), HttpServer)
    print("Server started http://%s:%s" % ("localhost", 8080))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped")