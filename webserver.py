from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>Hello!</body></html>"
				self.wfile.write(message)
				print message
				return
		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)

def main():
	try:
		port = 80
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()