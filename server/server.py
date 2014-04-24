#!/usr/bin/env python
"""
See http://pointlessprogramming.wordpress.com/2011/02/13/python-cgi-tutorial-1/
"""

import os
import sys

# Set script root in subprocesses
os.environ['SCRIPT_ROOT'] = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Modify cwd to allow this script to be run from anywhere
os.chdir(os.path.dirname(__file__))

import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting

server_address = ("", 8000)

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler

handler.cgi_directories = ["/deployment"]

httpd = server(server_address, handler)
httpd.serve_forever()
