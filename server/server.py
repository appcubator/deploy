#!/usr/bin/env python
"""
See http://pointlessprogramming.wordpress.com/2011/02/13/python-cgi-tutorial-1/
"""

# allows this script to be run from anywhere
import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))

import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting

server_address = ("", 8000)

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler

handler.cgi_directories = ["/deployment"]

httpd = server(server_address, handler)
httpd.serve_forever()
