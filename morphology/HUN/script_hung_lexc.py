
#!/usr/bin/python3
# -*- kodeketa: utf-8 -*-

# CSVak kudeatzeko:
import csv

Categ =['N','V','ADJ']

Suffix = ['ik']

def print_head():
	print("Lexicon Root")
	for c in Categ:
		print(c+"_lex ;")

def print_tail():
	for c in Categ:
		print("\nLexicon", c+"_morf"+"\n# ;")

input_file = "Hungarian00.csv"

print_head()
# 
with open(input_file, newline='') as csv_input:
	# sarrera fitxategia hiztegi batean kargatu
	reader_obj = csv.DictReader(csv_input)
	entries = list(reader_obj)
#	idazleguztiak = set()
	cat_prev="";
	for e in entries.copy():
		cat = e["Part of Speech"]
		stem = e["Stem"]
		lemma = stem
		for suf in Suffix:
			if stem.endswith(suf):
				l=len(suf)
				lemma = stem[:len(lemma)-l]
#				print(stem, lemma)
		if cat != cat_prev and cat in Categ:
			print("\nLexicon", cat+"_lex")
			cat_prev = cat
		if cat in Categ: 
	        	print(stem+":"+lemma+"\t"+cat+"_morf ;")
print_tail()

