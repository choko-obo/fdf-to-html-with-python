import os
import re
import docutils.core

btlcounter=0
emptylnecnt=1
newline='\r\n'
p_closed=1

path="moebel/testmoebel/"

with open('static/head') as h:
    for line in h:
        print(line)

scoreHeadingLevel = 0
underHeadingLevel = 0
tildeHeadingLevel = 0
equalHeadingLevel = 0
nextHeadingLevel = 2
got_title = 0
with open(path + "text.it") as f:
    for line in f:
        #check for the heading symbols 
        if re.search('(--+|__+|~~+|==+)$', line) != None:
            #Get title
            if got_title == 0:
                print('<div id="' + oldline + '">')
                got_title = 1

            if re.search('-+$', line) != None:
                if scoreHeadingLevel == 0:
                    scoreHeadingLevel = nextHeadingLevel
                    nextHeadingLevel += 1
                print('<h' + str(scoreHeadingLevel) + '>' + oldline + '</h' + str(scoreHeadingLevel) + '>')
            if re.search('_$', line) != None:
                if underHeadingLevel == 0:
                    underHeadingLevel = nextHeadingLevel
                    nextHeadingLevel += 1
                print('<h' + str(underHeadingLevel) + '>' + oldline + '</h' + str(underHeadingLevel) + '>')
            if re.search('~+$', line) != None:
                if tildeHeadingLevel == 0:
                    tildeHeadingLevel = nextHeadingLevel
                    nextHeadingLevel += 1
                print('<h' + str(tildeHeadingLevel) + '>' + oldline + '</h' + str(tildeHeadingLevel) + '>')
            if re.search('=+$', line) != None:
                if equalHeadingLevel == 0:
                    equalHeadingLevel = nextHeadingLevel
                    nextHeadingLevel += 1
                print('<h' + str(equalHeadingLevel) + '>' + oldline + '</h' + str(equalHeadingLevel) + '>')
        else

            oldline=line.replace(newline, '')
            #Check what we have
            #Is is a Image?
            if oldline[0] == '|':
                splitLine=oldline.replace('|','').split(';')
                print('<p><img src="' + path + splitLine[0] + '" alt="' + splitLine[1] + '""><br></p>')
            #Are those the footnotes
            elif re.search('^--', oldline) != None:
                if btlcounter == 0:
                    print('<p class="businesszeile">' + oldline.replace('--','') + '</p>')
                    btlcounter += 1
                elif btlcounter == 1:
                    print('<p class="unterschrift">' + oldline.replace('--','') + '</p>')
            #or a empty line?
            elif len(oldline) <= 2 and p_closed == 0:
                if emptylnecnt == 1:
                    emptylnecnt=2
                #two empty lines. close para
                elif emptylnecnt == 2:
                    p_closed=1
                    print('</p>')
                    emptylnecnt=1
                else:
                    emptylnecnt=1
            #or anything else
            else:
                #create a paragraph
                if p_closed == 1 and got_title == 1:
                    p_closed = 0
                    print('<p>')
                if oldline.find('(((') > 0:
                    #its a line with links
                    oline=""
                    cnt = 0 
                    while oldline.find('(((') > 0:
                        cnt += 1
                        splitLine=oldline.split('(((', 1)
                        oline=oline + splitLine[0]
                        splitLine=splitLine[1].split(')))', 1)
                        oline=oline + '<a href="' + splitLine[0].split(';')[0] + '">' + splitLine[0].split(';')[1] + '</a>'
                        oldline=splitLine[1]
                        #print oline
                    else:
                        oline=oline + oldline
                        print(oline + '<br>')

with open('static/tail') as t:
    for line in t:
        print(line)
