#
# Serve compressed files from the HTML directory
# so that the webrepl can be self hosted.
#
import re
import gc

try:
	import usocket as socket
except:
	import socket

#
# Send a reply to the connection
#
def http_reply(conn, code, content, gzip=False):
	print("HTTP response %d" % (code))
	conn.send('HTTP/1.1 %d OK\n' % (code))
	conn.send('Content-Type: text/html\n')
	if gzip:
		conn.send('Content-Encoding: gzip\n')
	conn.send('Connection: close\n\n')
	conn.sendall(content)
	
#
# Incoming connection: serve the pages to it
#
def http_server(s):
	conn, addr = s.accept()
	print('connect %s' % str(addr))
	request = str(conn.recv(1024))
	print('Content = %s' % request)

	# Look for a "GET /.... ...."
	m = re.search(r'GET /(.*?) ', request)
	if not m:
		http_reply(conn, 418, "Unknown command")
		conn.close()
		return

	name = m.group(1)
	if len(name) == 0:
		name = "index.html"

	try:
		print("GET " + name)
		f = open("html/" + name + ".gz", "rb")
		http_reply(conn, 200, '', gzip=True)

		# Can't read the entire file, so fetch it in pieces
		while True:
			d = f.read(1024)
			if not d:
				break
			conn.sendall(d)

		f.close()
	except:
		http_reply(conn, 404, name + ": not found")

	conn.close()

listen_sock = None

def start():
	global listen_sock
	listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_sock.bind(('', 80))
	listen_sock.listen(5)

	# setup the listener in the background
	listen_sock.setsockopt(socket.SOL_SOCKET, 20, http_server)

	print("web server on port 80")
	gc.collect()
