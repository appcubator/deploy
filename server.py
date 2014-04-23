#!/usr/bin/env python
"""
See http://pointlessprogramming.wordpress.com/2011/02/13/python-cgi-tutorial-1/
"""

import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting

server_address = ("", 8000)

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler

handler.cgi_directories = ["/cgi-bin"]

httpd = server(server_address, handler)
httpd.serve_forever()
