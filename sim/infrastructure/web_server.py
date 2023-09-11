import io
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import numpy as np
from PIL import Image

from sim.infrastructure.grid import Grid

host_name = "localhost"
server_port = 8080

grid: Grid = None


class HttpServer(BaseHTTPRequestHandler):

    # CORS settings
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        global grid

        if self.path == "/api/init":
            if grid is None:
                print(grid is None)
                print("create Grid")
                grid = Grid(600, 450, 50, 300)

            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(self.create_image().getvalue())
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        elif self.path == "/api/move":
            if grid is None:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            else:
                grid.step()
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(self.create_image().getvalue())
                self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        elif self.path == "/api/train":
            grid.train_creatures()
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(self.create_image().getvalue())
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))


    def create_image(self):
        array = np.zeros((450, 600, 3), dtype=np.uint8)
        data = grid.matrix

        for x in range(450):
            for y in range(600):
                if data[y][x] != 0:
                    array[x][y] = [0, 0, 0]
                else:
                    array[x][y] = [255, 255, 255]

        print("image")

        img = Image.fromarray(array)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        return img_byte_arr
