import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

class CDN(BaseHTTPRequestHandler):
    cache = {}

    def do_GET(self):
        url = self.path[1:]
        if url in self.cache:
            # Serve from cache
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.cache[url])
            print("Served from cache:", url)
        else:
            # Fetch from origin
            try:
                resp = urllib.request.urlopen(url)
            except Exception as e:
                self.send_error(502, str(e))
                return
            content = resp.read()
            self.cache[url] = content
            # Serve
            self.send_response(200)
            self.end_headers()
            self.wfile.write(content)
            print("Served from origin:", url)

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), CDN)
    print("Starting CDN server...")
    httpd.serve_forever()
    
'''
    To test the CDN code above, you can follow these steps:

Start the CDN server by running the Python code above. You can do this by running the command python cdn.py in your terminal, assuming the code is saved in a file named cdn.py.

Open a web browser and navigate to http://localhost:8080/http://example.com/image.jpg, where http://example.com/image.jpg is the URL of an image you want to fetch and cache.

The first time you visit the URL, the CDN server will fetch the image from the origin and cache it. The image will then be displayed in your web browser.

Refresh the web page to test if the image is served from the cache. The second time you visit the URL, the CDN server should serve the image from the cache without fetching it from the origin again.

You can also verify that the CDN server is caching the image by checking the console output. The first time you visit the URL, you should see a message saying "Served from origin" and the URL of the image. The second time you visit the URL, you should see a message saying "Served from cache" and the URL of the image.

Repeat the above steps with different URLs to test caching for multiple files.


'''