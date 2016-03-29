import httplib
import urllib

conn = httplib.HTTPConnection("192.168.207.254", 8086)
#params = urllib.urlencode({'q':'CREATE DATABASE mydb2'})
conn.request("GET", "/query?q=CREATE+DATABASE+mydb2")
#print params
#conn.request("GET", "/query?q=CREATE DATABASE mydb2")
response = conn.getresponse()

print response.status, response.reason
