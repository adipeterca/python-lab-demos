from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = f"""
<html>
  <body>
    <h1>Product Info</h1>

    <p>Price:</p>
    <p id="price">
      <span id="amount">12345</span>
      <span id="currency">RON</span>
    </p>
  </body>
</html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


print("Starting a webserver on http://127.0.0.1:8000 ...")
HTTPServer(("127.0.0.1", 8000), Handler).serve_forever() 