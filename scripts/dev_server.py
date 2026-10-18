#!/usr/bin/env python3
import functools
import http.server
import os
import socketserver
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Resolver ruta canónica base con SimpleHTTPRequestHandler
        translated = super().translate_path(path)
        # Si el archivo exacto no existe, pero existe con extensión .html, servir el .html
        if not os.path.exists(translated) and os.path.exists(translated + '.html'):
            return translated + '.html'
        return translated

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    handler = functools.partial(CleanURLHandler, directory=DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('0.0.0.0', port), handler) as httpd:
        print(f"Servidor de desarrollo macWave con soporte Clean URLs corriendo en http://0.0.0.0:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
