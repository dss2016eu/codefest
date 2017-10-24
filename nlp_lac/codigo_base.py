
import sys
import random
from lxml import etree
from nltk.corpus import wordnet

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'


f=open(sys.argv[1])
tree=etree.parse(f)
f.close()

langs = ['swe', 'fin', 'eus']
colors = {'swe':bcolors.HEADER, 'fin':bcolors.OKBLUE, 'eus':bcolors.OKGREEN}

wfs=tree.findall("//wf")

for wf in wfs:
    
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
		print colors[lang] + random.choice(lemmas) + bcolors.ENDC,
	else:
		print wf.text ,
    else:
	print wf.text,


#print wordnet.of2ss("ili-30-09284015-n")
