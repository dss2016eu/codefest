# preprocessing.py

Preprocesses an XML Wikipedia dump (from a single-file output of WikiExtract.py), removing short articles and articles collection w/ some extra cleanup + tokenization.

Usage:

`preprocessing.py xml_dump output.tsv dbpediacategories`

# readcorpus.py

Reads the tokenized and filtered wikipedia together with questions and plays the game.

Usage:

`readcorpus.py [-t|-d] wiki_corpus_file questions_file patterns_file`

The `-t` flag starts a self test to give statistics on all the questions.  The `-d` flag starts the demo for a human-computer match.

For example:

`readcorpus.py -d ./../EU/eu_tokenized_categorised_short.tsv ./../EU/short_questions.csv`

would run the demo with the Basque `short_questions.csv` file.
