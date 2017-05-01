#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

import os

# Create instance of FieldStorage 
form = cgi.FieldStorage() 


def TagList():
	print '<textarea name="textcontent" readonly cols="55" rows="25">'
	taglist = os.popen("tmsu tags").read().splitlines()
	if len(taglist)==0:
		print 'No tags present in database.'
	else:
		for item in taglist:
			print item
	print '</textarea>'
			

			
			
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Tag Search</title>"
print "</head>"
print "<body>"


print '<table>'
print '<form action="/cgi-bin/query.py" method="post">'
print '<input type="text" name="query" />'
print '<input type="submit" value="Search" />'
print '<input type="radio" name="option" value="display" /> Display Results'
print '<input type="radio" name="option" value="copy" /> Copy Results'
print '</form>'
print '</table>'

print '<table>'
print '<form action="/cgi-bin/append.py" method="post">'
print '<input type="submit" value="Append Files" />'
print '</form>'

print '<form action="/cgi-bin/tags.py" method="post">'
print '<input type="submit" value="Show Tags" />'
print '</form>'
print '</table>'

TagList()


print "</body>"
print "</html>"