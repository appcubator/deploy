#!/usr/bin/env python
import os

print "Content-type: text/html"
print
print "<title>Test CGI</title>"
print "<p>Hello World!</p>"
print "<p>Script root: {deploy_root}</p>".format(deploy_root=os.environ.get("SCRIPT_ROOT"))
