# preprocessing.py

Preprocesses an XML Wikipedia dump (from a single-file output of WikiExtract.py), removing short articles and articles collection w/ some extra cleanup + tokenization.

Usage:

`preprocessing.py xml_dump output.tsv dbpediacategories`

# readcorpus.py

Reads the tokenized and filtered wikipedia together with questions and plays the game.

Usage:

`readcorpus.py output.tsv question_file.csv`
