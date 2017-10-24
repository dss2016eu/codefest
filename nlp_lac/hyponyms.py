import sys
import random
from lxml import etree
from nltk.corpus import wordnet
import argparse

class bcolors:
	HEADER = '<a style="color:red">'
	OKBLUE = '<a style="color:blue">'
	OKGREEN = '<a style="color:green">'
	JUMP = '</br>'
	ENDC = '</a>'

#given a text, subtitutes the words that have a synset with their antonyms


##Available languages:

[u'als', u'arb', u'bul', u'cat', u'cmn',\
u'dan', u'ell', u'eng', u'eus', u'fas', u'fin',\
u'fra', u'fre', u'glg', u'heb', u'hrv', u'ind', u'ita',\
u'jpn', u'cat', u'eus', u'glg', u'spa', u'ind', u'zsm',\
u'nno', u'nob', u'nno', u'nob', u'pol', u'por', u'qcn', \
u'slv', u'spa', u'swe', u'tha', u'zsm']

#open necessary archives
f=open(sys.argv[1]) #parsed text with Ixa-pipes that contains the tale
fo=open(sys.argv[2],"w") #output, html format

parser = argparse.ArgumentParser(description='Transform the text using antonyms')
parser.add_argument('--lang', default='eng', help='Language of the antonyms')
parser.add_argument('--input', required=True, default='input.txt', help='file naf that contains the tagged and dissambiguated text')
parser.add_argument('--output', required=True, default='output.txt', help='file where the transformed text is going to be written')

args = parser.parse_args()

f= args.input
fo = args.output

lang1 = args.lang

tree=etree.parse(f)
f.close()

#color for the substituted words
colors = {'spa':bcolors.HEADER, 'eng':bcolors.OKBLUE}

##start
wfs=tree.findall("//wf")
parag_ant = 0

for wf in wfs:
	
	#keep paragraphs
	parag_act = wf.attrib['para']
	if parag_act != parag_ant:
		fo.write(bcolors.JUMP)
	
	#search words that have a synset
	expr="//term/span/target[@id='"+wf.attrib['id']+"']"
	term=tree.find(expr).getparent().getparent()
	wordsense = term.find("./externalReferences/externalRef")
	
	#if it has a sense
	if wordsense is not None:		
		ref = wordsense.attrib['reference']
		ref = ref.replace('ili-30-','')
		syn = wordnet.of2ss(ref)

		
		try:
	
			hypo = syn.hyponyms()[0]
			lemma = hypo.lemma_names(lang1)[0]
			fo.write(colors[lang1] + lemma.encode('utf8') +  bcolors.ENDC + " ")
			
			
		except:
			#if something goes wrong, write the original word
			fo.write(wf.text.encode('utf8') + " ")
				
	else:
		#if there is no synset associated, write original word
		fo.write(wf.text.encode('utf8') + " ")
	parag_ant = parag_act

fo.close()
