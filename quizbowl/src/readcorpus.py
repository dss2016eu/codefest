import codecs
import sys
from collections import Counter
import math


class Article:

    def __init__(self, title, category, words):
        self.title = title
        self.category = category
        self.wordcounts = Counter(words)
        self.vocab = set(self.wordcounts.keys())
        for w in words:
            self.wordcounts[w] = self.wordcounts.get(w, 0) + 1
        self.length = sum(self.wordcounts.values())
        self.tfidf = {}
        self.norm = 0                  # |A|, needed for quick cosine
        self.termfreqencies = {word: self.wordcounts[word] / float(self.length) for word in self.vocab}

    def compute_norm(self):
        self.norm = math.sqrt(sum([val**2 for val in self.tfidf.values()]))

    def dotproduct(self, other):
        common_vocab = self.vocab.intersection(other.vocab)
        return sum(self.tfidf[word] * other.tfidf[word] for word in common_vocab)

    def similarity(self, other):
        """Calculate cosine between two articles."""
        return self.dotproduct(other) / float(self.norm * other.norm)

    def update_tfidf(self, doccount, docfrequencies):
        for word in self.vocab:
            self.tfidf[word] = math.log(doccount / float(docfrequencies[word])) * self.wordcounts[word]
        self.compute_norm()


class Wiki:

    def __init__(self):
        self.articles = set()
        self.docfrequencies = {}        # {"word": (word count in corpus, documents containing word)}
        self.articlecount = 0

    def add_article(self, article):
        self.articles.add(article)
        self.articlecount += 1
        self.update_docfrequencies(article)      # update document frequencies

    def update_docfrequencies(self, article):
        for word in article.vocab:
            self.docfrequencies[word] = self.docfrequencies.get(word, 0) + 1

    def vocab(self):
        return self.docfrequencies.keys()

    def update_tfidf(self):     # call when all articles have been added to the collection
        for article in self.articles:
            article.update_tfidf(self.articlecount, self.docfrequencies)


def article_streamer(input_path, token_separator="|", debug_limit=None):
    with codecs.open(input_path) as f:
        for index, article in enumerate(f):
            split = article.strip().split("\t")
            title = split[0]
            category = split[1]
            tokens = split[-1].split(token_separator)
            yield title, category, tokens

            if debug_limit is not None and index >= debug_limit:
                break

def create_wiki(input, debug_limit=None):
    wiki = Wiki()
    for title, cat, tokens in article_streamer(input, debug_limit=debug_limit):
        article = Article(title, cat, tokens)
        wiki.add_article(article)

    wiki.update_tfidf()
    return wiki



if __name__ == '__main__':

    input = sys.argv[1]
    wiki = create_wiki(input, debug_limit=100)

    previous_article = None

    for article in wiki.articles:
        print(article.title)
        print(len(article.vocab))
        print(article.tfidf.items()[:10])
        print(article.norm)
        print("cosine with previous article")
        print(article.similarity(previous_article if previous_article is not None else article))
        print("\n")
        previous_article = article


