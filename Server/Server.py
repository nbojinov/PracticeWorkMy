from os import curdir,sep
import urllib
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
import time

# Port on which server will run.
PORT = 50007


class HTTPRequestHandler(BaseHTTPRequestHandler):

	res=False
	Result=0
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		
		txt=""
		if s.path=="/":
			typeOfData='text/html'
			Str="""
	<html>
		<head>
			<title>SUM</title>
		</head> 
		<body>
			<form method="post">
	  			First number: <input type="text" name="fnum"><br>
	  			Second number: <input type="text" name="lnum"><br>
				<br/>
				+: <input type="radio" name="sign" value="+" checked=true><br>
	  			-: <input type="radio" name="sign" value="-"><br>
				*: <input type="radio" name="sign" value="*"><br>
	  			<input type="submit" value="Submit">
			</form> """
			if s.res:
				Str+=str(s.Result)
				s.res=False
			Str+="""		 
		</body>
	</html>"""
			txt=bytes(Str,'UTF-8')
			
		else:
			try:
				send = False
				if s.path.endswith(".html"):
					typeOfData='text/html'
					send = True
				elif (s.path.endswith(".jpg") or s.path.endswith(".jpeg")):
					typeOfData='image/jpg'
					send = True
				elif (s.path.endswith(".py")):
					typeOfData='text/html'
					with open(curdir + sep + s.path) as f1:
						old_stdout=sys.stdout
						temp=StringIO()
						sys.stdout=temp
						
						code = compile(f1.read(), curdir + sep + s.path, 'exec')
						exec(code)

						txt=temp.getvalue()
						sys.stdout=old_stdout

						txt=bytes(txt,'UTF-8')
						s.send_response(200)
						s.send_header('Content-type',typeOfData)
						s.end_headers()
						s.wfile.write(txt)
						return
				if send == True: 
					f = open(curdir + sep + s.path,mode="rb")
					txt=f.read()
					f.close()
				else:
					print ("here")	
					return

			except IOError:
				s.send_error(404,'File Not Found: %s' % s.path)
		s.send_response(200)
		s.send_header('Content-type',typeOfData)
		s.end_headers()
		s.wfile.write(txt)

	def do_POST(s):
		length = int(s.headers['Content-Length'])
		post_data = urllib.parse.parse_qs(s.rfile.read(length).decode('utf-8'))
		s.res=True
		if('fnum' in post_data and 'lnum' in post_data):
			if(post_data['sign'][0]=="+"):
				s.Result=int(post_data['fnum'][0])+int(post_data['lnum'][0])
			elif(post_data['sign'][0]=="-"):
				s.Result=int(post_data['fnum'][0])-int(post_data['lnum'][0])
			elif(post_data['sign'][0]=="*"):
				s.Result=int(post_data['fnum'][0])*int(post_data['lnum'][0])
		else:
			s.Result='You have missed to fill in a field'
		s.do_GET()

if __name__ == '__main__':
	print (curdir)
	if(len(sys.argv)>1):
		PORT=int(sys.argv[1])
	handler=HTTPRequestHandler
	handler.cgi_directories = ['/cgi-bin']
	HTTPDeamon = HTTPServer(('', PORT), handler)

	print("Listening at port", PORT)

	try:
		HTTPDeamon.serve_forever()
	except KeyboardInterrupt:
		pass

	HTTPDeamon.server_close()
	print("Server stopped")
