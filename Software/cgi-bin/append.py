#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# for accessing files in directory tree
import os
# for copying files
import shutil
# for easy substring substitution
import re
# for interfacing with TMSU through CLI
import commands

# Create instance of FieldStorage 
form = cgi.FieldStorage()

query_dir = "QUERIES"
os.popen("cd ..")


def Tagger():
	counter = 0
	os.popen("cd ..")
	#create database (if not already created)
	cmd = "tmsu.exe init"
	os.popen(cmd)

	#get list of tagged files in the database
	filelist = []
	cmd = "tmsu.exe files"
	filelist = os.popen(cmd).read().splitlines()

	#get list of *.asc files
	for dirpath, dirnames, filenames in os.walk("."):
		for filename in [f for f in filenames if f.endswith(".asc")]:
			
			#variable decarations, it is necessary that the lists be reinitialized between files
			eoh="*********************************end of header"
			parse=[]
			tag=[]
			value=[]
			param=""
			
			#access file in working directory
			filename = os.path.join(dirpath, filename)
			#ignore raw data, and only tag files not already tagged, (NEW) also ignores query results directory
			if "raw" not in filename and filename not in filelist and query_dir not in filename:
				
				print(filename)
				#open one file
				f = open(filename, 'r')
				#read file until end of header indicator is reached
				for line in f.readlines():
					if eoh in line:
						break
					else:
						parse.append(line)

				#parse for tags and values
				for i in xrange(0,len(parse)):

					#replace or remove illegal characters, i.e. "/", "(", ")"
					parse[i]=parse[i].replace("/","-")
					parse[i]=parse[i].replace("(","_")
					parse[i]=parse[i].replace(")","")

					#for most tags, look for ": " as tag separator
					offset = parse[i].find(": ")
					if offset != -1:
						tag_temp = parse[i][:offset]
						value_temp = parse[i][offset+2:]
						#tags must be single words for use in TMSU
						tag_temp = tag_temp.replace(" ","_")
						tag.append(tag_temp)
						#interpret spaces as multiple tag values
						value_temp = value_temp.replace(" - "," ")
						value_temp = value_temp.replace(" *End of laser names","")
						value.append(re.sub("[ ]"," ",value_temp).split())

					#special case for blank comment
					elif parse[i].find(":") != -1 and parse[i][len(parse[i]):]=="":
						offset = parse[i].find(":")
						tag.append(parse[i][:offset])
						value.append("")

					#special case for probe/other temp
					else:
						parse[i] = parse[i].replace(" ","_")
						while True:
							off1 = parse[i].find("____")
							prestr = parse[i][:off1]
							off2 = prestr.find("_-_")
							tag.append(parse[i][:off2])
							value.append(re.sub("","",parse[i][off2+3:off1]).split())
							#multiple segments remaining
							if off1 != -1:
								parse[i] = parse[i][off1+4:]
							#final segment
							else:
								break

				#generate tag[i]=value[i][j] string
				for i in xrange(0,len(value)):
					for j in xrange(0,len(value[i])):
						param+=str(tag[i]+"="+value[i][j]+" ")
				#remove the space at the end
				param = param[:len(param)-1]
				#generate command to apply tags and values to file through TMSU
				cmd = str("tmsu.exe tag \""+filename+"\" "+param)
				#execute command
				print(os.popen(cmd).read())
				counter = counter+1
	return counter

def Append():
	print '<textarea name="textcontent" readonly cols="55" rows="25">'
	counter=Tagger()
	print 'Newly tagged files: '+str(counter)+"."
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

Append()




print "</body>"
print "</html>"