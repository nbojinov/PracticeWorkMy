import cgi
import cgitb; cgitb.enable()

print("<html><body>")
for i in range(0,100):
	print(i,"<br>")
print("</body></html>")
