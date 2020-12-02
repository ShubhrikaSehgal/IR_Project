# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:39:36 2020

@author: 16303
"""
import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('Search')
print("Content-type:text/html")
print
print("")
print("")
print("Hello - Second CGI Program")
print("")
print("")
print("Hello %s %s" % (searchterm))
print("")
print("")