import Image
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import threading
import Queue

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			q = self.server.subscribe()
			while True:
					jpg = q.get()
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(jpg))
					self.end_headers()
					self.wfile.write(jpg)
					time.sleep(0.05)
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="/screen.mjpg"/>')
			self.wfile.write('</body></html>')
			return


class ThreadedImageStreamServer(ThreadingMixIn, HTTPServer):
	def __init__(self, addr=('localhost', 8080)):
		super(ThreadedImageStreamServer, self).__init__(addr, Handler)
		self.qs=set()
		self.lastimg=None
		self.serve_forever()
		self.lock=threading.Lock()

	def subscribe(self):
		with self.lock:
			q = Queue.Queue()
			self.qs.add(q)
			if self.lastimg !=None:
				q.put(self.lastimg)

	def sendImage(self, img):
		tmpFile = StringIO.StringIO()
		img.save(tmpFile,'JPEG')
		jpg = tmpFile.getvalue()
		tmpfile.close()
		with self.lock:
			self.lastimg = jpg
			for q in self.qs:
				q.put(jpg)
