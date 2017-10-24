
import sys
import random
import largefile
import requests
#Manual at http://lxml.de/tutorial.html
from lxml import etree
#Manual: http://www.nltk.org/howto/wordnet.html
#Extended wordnets from http://compling.hss.ntu.edu.sg/omw/summx.html
from nltk.corpus import wordnet

se=largefile.Searcher('/Users/manex/Downloads/fall11_urls.txt')

MAXTRIALS=5
#class bcolors:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKGREEN = '\033[92m'
#    JUMP = '\n'
#    ENDC = '\033[0m'

#class bcolors:
#	HEADER = '<a style="color:#%02x%02x%02x>' % (r,g,b)
#	OKBLUE = '<a style="color:#0000FF">'
#	OKGREEN = '<a style="color:#00FF00">'
#	JUMP = '</br>'
#	ENDC = '</a>'


f=open(sys.argv[1])
fo=open(sys.argv[2],"w")
tree=etree.parse(f)
f.close()

langs=['spa']

#http://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
colors={}
for lang in langs:
  r,g,b=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
  colors[lang]='<a style="color:#%02x%02x%02x">' % (r,g,b)

colors['ENDC']='</a>'
colors['JUMP']='</br>'

wfs=tree.findall("//wf")

parag_ant = 0

for wf in wfs:
    
    parag_act = wf.attrib['para']
    if parag_act != parag_ant:
        fo.write(colors['JUMP'])
    expr="//term/span/target[@id='"+wf.attrib['id']+"']"
    term=tree.find(expr).getparent().getparent()
    wordsense = term.find("./externalReferences/externalRef")
    if wordsense is not None:
        ref = wordsense.attrib['reference']
        ref=ref.replace("ili-30-","")
        syn = wordnet.of2ss(ref)
        lang = random.choice(langs)
        lemmas = syn.lemma_names(lang)
#	print lemmas
#	if len(lemmas) != 0:
        #p=random.random()
        if lemmas:# and p<0.5:
#            fo.write(colors[lang] + random.choice(lemmas).encode('utf8') + colors['ENDC'] + " ")
#        else:
            ok=0
            wsens = ref[-1]+ref[0:-3]
            trials=0
            while(ok == 0 and trials<MAXTRIALS):
                urls=se.find(wsens)
                if len(urls) == 0:
                    fo.write(wf.text.encode('utf8') + " ")
                    break
                lineimg = random.choice(urls)
                path = lineimg.split('\t')[1]
                print path
                #raw_input()
                try:
                    r = requests.head(path)
                    if r.status_code == requests.codes.ok:
                        fo.write("<img src=\""+path+"\"  width=\"200\" height=\"200\"/>")
                        ok = 1
                    else:
                        ok = 0
                except requests.exceptions.ConnectionError:
                    fo.write("<img src=\""+path+"\"/>")
                    ok = 1
                trials=trials+1
            print "Bieeen"
    else:
        fo.write(wf.text.encode('utf8') + " ")
    parag_ant = parag_act

fo.close()


#print wordnet.of2ss("ili-30-09284015-n")
