#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 
# for accessing files in directory tree
import os
# for copying files
import shutil

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
query = form.getvalue('query')
option = form.getvalue('option')

query_dir = "QUERIES"

def Query(query):
	print '<textarea name="textcontent" readonly cols="55" rows="25">'
	print 'Search term: %s\n' % query
	filelist = os.popen("tmsu files "+str(query)).read().splitlines()
	if len(filelist)==0 or query=="":
		print 'No files with these search terms present in database.'
	else:
		for item in filelist:
			print item
	print '</textarea>'
	
def Copy(query):
	print '<textarea name="textcontent" readonly cols="55" rows="25">'
	print 'Search term: %s\n' % query
	filelist = os.popen("tmsu files "+query).read().splitlines()
	if len(filelist)==0 or query=="":
		print 'No files with these search terms present in database.'
	else:
		counter = 0
		dst = query_dir+os.sep+query
		if not os.path.exists(dst):
			os.makedirs(dst)
		filelist = os.popen("tmsu files "+query).read().splitlines()
		for src in filelist:
			#print(src)
			shutil.copy2(src, dst)
			counter=counter+1
		print str(counter)+' files copied to .'+os.sep+dst
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

if option:
	if option == "display":
		Query(query)
	elif option == "copy":
		Copy(query)
else:
	print '<textarea name="textcontent" readonly cols="55" rows="25">'
	print 'Select how to show search results.'
	print '</textarea>'


print "</body>"
print "</html>"