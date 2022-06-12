import io
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from infrastructure.grid import Grid
import numpy as np
from PIL import Image

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
        if grid is None:
            print(grid is None)
            print("create Grid")
            grid = Grid(600, 450, 5000, 300)

        grid.step()

        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()
        self.wfile.write(self.create_image().getvalue())
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))

    def create_image(self):
        global grid
        array = np.zeros((450, 600, 3), dtype=np.uint8)
        data = grid.step()

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