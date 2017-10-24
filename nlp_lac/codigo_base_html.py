
import sys
import random
from lxml import etree
from nltk.corpus import wordnet

#class bcolors:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKGREEN = '\033[92m'
#    JUMP = '\n'
#    ENDC = '\033[0m'

class bcolors:
	HEADER = '<a style="color:red">'
	OKBLUE = '<a style="color:blue">'
	OKGREEN = '<a style="color:green">'
	JUMP = '</br>'
	ENDC = '</a>'


f=open(sys.argv[1])
fo=open(sys.argv[2],"w")
tree=etree.parse(f)
f.close()

langs = ['swe', 'glg', 'fin']
colors = {'swe':bcolors.HEADER, 'glg':bcolors.OKBLUE, 'fin':bcolors.OKGREEN}

wfs=tree.findall("//wf")

parag_ant = 0

for wf in wfs:
    
    parag_act = wf.attrib['para']
    if parag_act != parag_ant:
	fo.write(bcolors.JUMP)
    #print wf.attrib['id']
    expr="//term/span/target[@id='"+wf.attrib['id']+"']"
    #print expr
    term=tree.find(expr).getparent().getparent()
    wordsense = term.find("./externalReferences/externalRef")
    if wordsense is not None:
        ref = wordsense.attrib['reference']
	syn = wordnet.of2ss(ref)
	lang = random.choice(langs)
	lemmas = syn.lemma_names(lang)
	if len(lemmas) != 0:
		fo.write(colors[lang] + random.choice(lemmas).encode('utf8') + bcolors.ENDC + " ")
	else:
		fo.write(wf.text.encode('utf8') + " ")
    else:
	fo.write(wf.text.encode('utf8') + " ")
    parag_ant = parag_act

fo.close()


#print wordnet.of2ss("ili-30-09284015-n")
