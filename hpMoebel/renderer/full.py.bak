import os

got_title=0
btlcounter=0
emptylnecnt=1
newline='\r\n'
p_closed=1

path="moebel/testmoebel/"

with open('static/head') as h:
    for line in h:
        print line

with open(path + "text.it") as f:
    for line in f:
    	sline=line.replace(newline, '')
    	#Check what we have
    	#Is is a Image?
    	if line[0] == '|':
    		splitLine=sline.replace('|','').split(';')
    		print '<p><img src="' + path + splitLine[0] + '" alt="' + splitLine[1] + '""><br></p>'
    	#Are those the footnotes
    	elif line[0] + line[1] == '--':
    		if btlcounter == 0:
    			print '<p class="businesszeile">' + sline.replace('--','') + '</p>'
    			btlcounter += 1
    		elif btlcounter == 1:
    			print '<p class="unterschrift">' + sline.replace('--','') + '</p>'
    	#or a empty line?
    	elif len(line) <= 2 and p_closed == 0:
    		if emptylnecnt == 1:
    			emptylnecnt=2
    		#two empty lines. close para
    		elif emptylnecnt == 2:
    			p_closed=1
    			print '</p>'
    			emptylnecnt=1
    		else:
    			emptylnecnt=1
    	#or anything else
    	else:
    		#create a paragraph
    		if p_closed == 1 and got_title == 1:
    			p_closed = 0
    			print '<p>'
	    	if sline.find('(((') > 0:
	    		#its a line with links
	    		oline=""
	    		cnt = 0 
	    		while sline.find('(((') > 0:
	    			cnt += 1
	    			splitLine=sline.split('(((', 1)
	    			oline=oline + splitLine[0]
	    			splitLine=splitLine[1].split(')))', 1)
	    			oline=oline + '<a href="' + splitLine[0].split(';')[0] + '">' + splitLine[0].split(';')[1] + '</a>'
	    			sline=splitLine[1]
	    			#print oline
	    		else:
	    			oline=oline + sline
	    			print oline + '<br>'
	    	else:
				#Get title
		    	if got_title == 0:
		    		print '<div id="' + sline + '">'
		    		print '<h2>' + sline + '</h2>'
		    		got_title = 1
		    	else:
		    		if len(line) > 2:
	    				print sline + '<br>'

with open('static/tail') as t:
    for line in t:
        print line
